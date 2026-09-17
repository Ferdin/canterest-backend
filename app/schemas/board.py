from pydantic import BaseModel
from typing import Optional

class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_secret: bool = False

class BoardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_secret: Optional[bool] = None

class BoardOut(BoardCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True    