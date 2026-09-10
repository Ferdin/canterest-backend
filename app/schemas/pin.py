from pydantic import BaseModel, ConfigDict
from typing import Optional

class PinCreate(BaseModel):
    media_url: str #required
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

class PinOut(PinCreate):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
            