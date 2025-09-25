# app/models/token.py
import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    token_hash = Column(String, nullable=False)  # <-- store hashed token, not raw
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    revoked = Column(String, default="false")    # optional flag
