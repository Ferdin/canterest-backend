from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from app.database import Base

class PinLike(Base):
    __tablename__ = "pin_likes"

    # One like per user per pin: the pair is the primary key.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    pin_id = Column(Integer, ForeignKey("pins.id", ondelete="CASCADE"), primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())