from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User 
from app.schemas.user import PublicUserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}", response_model=PublicUserOut)
def get_user_by_username(username:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(404, "User not defined")
    return user    