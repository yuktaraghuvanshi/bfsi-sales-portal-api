# app/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, func, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(80), nullable=False, unique=True)
    email = Column(String(254), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String(20), nullable=False, default="sales")
    full_name = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    refresh_token_hash = Column(String, nullable=True)  # 🔹 store hashed refresh token
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_users_role", "role"),
    )
