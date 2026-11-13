from sqlalchemy.orm import Session, selectinload
from app.models.pin import Pin
from app.schemas.pin import PinCreate
from datetime import datetime, timedelta, timezone

from app.models.comment import Comment
from app.models.pin_like import PinLike

def count_likes(db: Session, pin_id: int) -> int:
    return db.query(PinLike).filter(PinLike.pin_id == pin_id).count()


def has_liked(db: Session, pin_id: int, user_id: int) -> bool:
    return db.get(PinLike, (user_id, pin_id)) is not None


def like_pin(db: Session, pin_id: int, user_id: int) -> None:
    # Liking twice is harmless: only add a row if there isn't one.
    if not has_liked(db, pin_id, user_id):
        db.add(PinLike(user_id=user_id, pin_id=pin_id))
        db.commit()


def unlike_pin(db: Session, pin_id: int, user_id: int) -> None:
    like = db.get(PinLike, (user_id, pin_id))
    if like is not None:
        db.delete(like)
        db.commit()


def list_comments(db: Session, pin_id: int) -> list[Comment]:
    return (
        db.query(Comment)
        .options(selectinload(Comment.author))
        .filter(Comment.pin_id == pin_id)
        .order_by(Comment.created_at, Comment.id)
        .all()
    )


def add_comment(db: Session, pin_id: int, author_id: int, body: str) -> Comment:
    comment = Comment(pin_id=pin_id, author_id=author_id, body=body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def _purge_expired_drafts(db: Session, owner_id: int | None = None):
    cutoff = datetime.now(timezone.utc) - timedelta(days=DRAFT_EXPIRATION_DAYS)
    query = db.query(Pin).filter(Pin.status == "draft", Pin.created_at < cutoff)
    if owner_id is not None:
        query = query.filter(Pin.owner_id == owner_id)
    query.delete(synchronize_session=False)
    db.commit()    

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
        