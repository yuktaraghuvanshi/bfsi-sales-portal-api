# app/crud/user.py
from sqlalchemy.orm import Session
from app import models
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------
# Password helpers
# ---------------------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------------------
# User CRUD
# ---------------------
def get_user(db: Session, user_id):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_in: UserCreate):
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        full_name=user_in.full_name,
        phone=user_in.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id):
    obj = db.query(models.User).filter(models.User.user_id == user_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj

# ---------------------
# Refresh Token helpers
# ---------------------
def set_refresh_token(db: Session, user: models.User, refresh_token: str):
    """Hash and store refresh token"""
    user.refresh_token_hash = get_password_hash(refresh_token)
    db.commit()
    db.refresh(user)
    return user

def verify_refresh_token(user: models.User, refresh_token: str) -> bool:
    """Verify provided refresh token"""
    if not user.refresh_token_hash:
        return False
    return verify_password(refresh_token, user.refresh_token_hash)

def revoke_refresh_token(db: Session, user: models.User):
    """Revoke (clear) refresh token"""
    user.refresh_token_hash = None
    db.commit()
    db.refresh(user)
    return user
