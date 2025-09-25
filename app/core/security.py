from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_token(token: str) -> str:
    """Hash a refresh token for storage"""
    return pwd_context.hash(token)

def verify_token(token: str, hashed: str) -> bool:
    """Verify a refresh token"""
    return pwd_context.verify(token, hashed)
