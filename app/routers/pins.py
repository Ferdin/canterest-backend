from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.pin import PinCreate, PinOut
from app.services import pin_service

router = APIRouter(prefix="/pins", tags=["pins"])

@router.post("", response_model=PinOut)
def create_pin(
    payload: PinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return pin_service.create_pin(db, owner_id=current_user.id, payload=payload)

@router.get("", response_model=list[PinOut])
def list_pins(db: Session = Depends(get_db)):
    return pin_service.get_pins(db)

@router.get("/{pin_id}", response_model=PinOut)
def get_pin(pin_id: int, db: Session = Depends(get_db)):
    pin = pin_service.get_pin(db, pin_id)
    if not pin:
        raise HTTPException(404, "Pin not found")
    return pin        