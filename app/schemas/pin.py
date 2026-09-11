from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime, timedelta, timezone
from typing import Optional

DRAFT_EXPIRATION_DAYS = 30

class PinCreate(BaseModel):
    media_url: str #required
    status: Optional[str] = "draft"
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    board_id: Optional[str] = None
    topics: Optional[list[str]] = None
    tagged_products: Optional[list[str]] = None
    alt_text: Optional[str] = None
    mark_as_ai_modified: bool = False
    includes_ai_generated_person: bool = False
    allow_comments: bool = True
    show_similar_products: bool = True

class PinUpdate(BaseModel):
    # everything optional - used for both "fill in more fields" and publish
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    board_id: Optional[str] = None
    topics: Optional[list[str]] = None
    tagged_products: Optional[str] = None
    alt_text: Optional[str] = None
    mark_as_ai_modified: Optional[str] = None
    includes_ai_generated_person: Optional[bool] = None
    allow_comments: Optional[bool] = None
    show_similar_products: Optional[bool] = None

class PinOut(PinCreate):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def days_until_expiration(self) -> Optional[int]:
        if self.status != "draft":
            return None

        created = self.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)    

        expires_at = created + timedelta(days=DRAFT_EXPIRATION_DAYS)
        remaining = (expires_at - datetime.now(timezone.utc)).days
        return max(remaining, 0)    
            