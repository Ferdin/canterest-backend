from sqlalchemy.orm import Session
from app.models.pin import Pin
from app.schemas.pin import PinCreate

def create_pin(db: Session, owner_id: int, payload: PinCreate) -> Pin:
    pin = Pin(owner_id=owner_id, **payload.model_dump())
    db.add(pin)
    db.commit()
    db.refresh(pin)
    return pin

def update_pin(db: Session, pin_id: int, owner_id: int, payload: PinUpdate) -> Pin | None:
    pin = db.query(Pin).filter(Pin.id == pin_id, Pin.owner_id == owner_id).first()
    if not pin:
        return None

    updates = payload.model_dump(exclude_unset=True)  # only fields actually sent
    for field, value in updates.items():
        setattr(pin, field, value)

    db.commit()
    db.refresh(pin)
    return pin

def get_pins(db: Session, owner_id: int | None = None, status: str | None = None) -> list[Pin]:
    query = db.query(Pin)
    if owner_id is not None:
        query = query.filter(Pin.owner_id == owner_id)
    if status is not None:
        query = query.filter(Pin.status == status)
    return query.order_by(Pin.created_at.desc()).all()

def get_pin(db: Session, pin_id: int) -> Pin | None:
    return db.query(Pin).filter(Pin.id == pin_id).first()
        