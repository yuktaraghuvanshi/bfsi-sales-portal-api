# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from datetime import datetime, timedelta
import secrets

from app import schemas
from app.crud import user
from app.db import get_db
from app.schemas.user import UserCreate, UserOut, RefreshRequest

router = APIRouter(prefix="/users", tags=["users"])

# ---------------------
# Login Rate-Limit Config
# ---------------------
login_attempts = {}
MAX_ATTEMPTS = 3
BLOCK_TIME = timedelta(minutes=5)

def check_login_attempt(username: str):
    attempts, last_time = login_attempts.get(username, (0, datetime.min))
    if attempts >= MAX_ATTEMPTS:
        if datetime.now() - last_time < BLOCK_TIME:
            raise HTTPException(
                status_code=429,
                detail=f"Too many login attempts. Try again after {BLOCK_TIME.total_seconds()//60} minutes."
            )
        else:
            login_attempts[username] = (0, datetime.now())

# ---------------------
# Login Schema
# ---------------------
class LoginSchema(BaseModel):
    username: str
    password: str

# ---------------------
# Login Endpoint
# ---------------------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    check_login_attempt(data.username)

    db_user = user.get_user_by_username(db, data.username)
    if not db_user or not user.verify_password(data.password, db_user.hashed_password):
        attempts, _ = login_attempts.get(data.username, (0, datetime.now()))
        login_attempts[data.username] = (attempts + 1, datetime.now())
        raise HTTPException(status_code=401, detail="Invalid username or password")

    login_attempts[data.username] = (0, datetime.now())

    # Create JWT tokens
    access_token = Authorize.create_access_token(subject=str(db_user.user_id))
    refresh_token = secrets.token_urlsafe(32)  # 🔹 plain refresh token
    user.set_refresh_token(db, db_user, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": db_user,
    }

# ---------------------
# Refresh Endpoint
# ---------------------
@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(user.models.User).filter(user.models.User.refresh_token_hash.isnot(None)).first()
    if not db_user or not user.verify_refresh_token(db_user, payload.refresh_token):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = Authorize.create_access_token(subject=str(db_user.user_id))
    return {"access_token": new_access_token}

# ---------------------
# Logout Endpoint
# ---------------------
@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    db_user = db.query(user.models.User).filter(user.models.User.refresh_token_hash.isnot(None)).first()
    if db_user and user.verify_refresh_token(db_user, data.refresh_token):
        user.revoke_refresh_token(db, db_user)
    return {"msg": "Logged out successfully"}

# ---------------------
# User CRUD Endpoints
# ---------------------
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if user.get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return user.create_user(db, payload)

@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return user.list_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    u = user.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u
