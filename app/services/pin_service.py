from sqlalchemy.orm import Session
from app.models.pin import Pin
from app.schemas.pin import PinCreate

def create_pin(db: Session, owner_id: int, payload: PinCreate) -> Pin:
    pin = Pin(owner_id=owner_id, **payload.model_dump())
    db.add(pin)
    db.commit()
    db.refresh(pin)
    return pin

def get_pins(db: Session, skip: int = 0, limit: int = 50) -> list[Pin]:
    return db.query(Pin).order_by(Pin.created_at.desc()).offset(skip).limit(limit).all()

def get_pin(db: Session, pin_id: int) -> Pin | None:
    return db.query(Pin).filter(Pin.id == pin_id).first()
        