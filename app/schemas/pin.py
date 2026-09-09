from pydantic import BaseModel
from typing import optional

class PinCreate(BaseModel):
    media_url: str #required
    title: Optional[str] = None
    description: Optional[str] = None
    link: Optional[str] = None
    board_id: Optional[str] = None
    topics: Optinal[str] = None
    tagged_products: Optinal[str] = None
    alt_text: Optional[str] = None
    mark_as_ai_modified: bool = False
    includes_ai_generated_person: bool = False
    allow_comments: bool = True
    show_similar_products: bool = True

class PinOut(PinCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
            