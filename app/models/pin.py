from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.database import Base

class Pin(Base):
    __tablename__ = "pins"

    id = Column(Integer, primary_key=True, index=True)

    # required
    media_url = Column(String, nullable=False)
    status = Column(String, default="draft", nullable=False)

    # optional fields from the creation form
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    link = Column(String, nullable=True)
    board_id = Column(Integer, nullable=True) # ForeignKey("boards.id") in the middle of the Column after creating the Board Model
    topics = Column(JSON, nullable=True)
    tagged_products = Column(JSON, nullable=True)
    alt_text = Column(String, nullable=True)

    # boolean toggles - default to sensible values matching the form
    mark_as_ai_modified = Column(Boolean, default=False, nullable=False)
    includes_ai_generated_person = Column(Boolean, default=False, nullable=False)
    allow_comments = Column(Boolean, default=True, nullable=False)
    show_similar_products = Column(Boolean, default=True, nullable=False)

    # ownership + metadata
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="pins")