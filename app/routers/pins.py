from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional
from app.models.user import User
from app.schemas.pin import PinCreate, PinUpdate, PinOut
from app.services import pin_service

router = APIRouter(prefix="/pins", tags=["pins"])

@router.post("", response_model=PinOut)
def create_pin(
    payload: PinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return pin_service.create_pin(db, owner_id=current_user.id, payload=payload)

@router.patch("/{pin_id}", response_model=PinOut)
def update_pin(
    pin_id: int,
    payload: PinUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pin = pin_service.update_pin(db, pin_id, owner_id=current_user.id, payload=payload)
    if not pin:
        raise HTTPException(404, "Pin not found")
    return pin    

@router.get("", response_model=list[PinOut])
def list_pins(
    status: str | None = None,
    mine: bool = False,
    username: str | None = None,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    owner_id = None

    if mine:
        if not current_user:
            raise HTTPException(401, "Not authenticated")
        owner_id = current_user.id
    elif username:
        target_user = db.query(User).filter(User.username == username).first()
        if not target_user:
            raise HTTPException(404, "User not found")
        owner_id = target_user.id
        status = status or "published" # public viewers only see published pins by default
    return pin_service.get_pins(db, owner_id=owner_id, status=status)

@router.get("/{pin_id}", response_model=PinOut)
def get_pin(pin_id: int, db: Session = Depends(get_db)):
    pin = pin_service.get_pin(db, pin_id)
    if not pin:
        raise HTTPException(404, "Pin not found")
    return pin        