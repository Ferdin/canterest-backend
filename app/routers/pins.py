from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user, get_current_user_optional
from app.models.pin import Pin
from app.models.user import User
from app.schemas.pin import (
    CommentCreate,
    CommentOut,
    PinCreate,
    PinDetail,
    PinOut,
    PinUpdate,
    PinUser,
)
from app.services import pin_service

router = APIRouter(prefix="/pins", tags=["pins"])


def get_visible_pin(db: Session, pin_id: int, current_user: User | None) -> Pin:
    """A pin anyone may see: published pins, plus your own drafts."""
    pin = pin_service.get_pin(db, pin_id)
    is_owner = current_user is not None and current_user.id == pin.owner_id if pin else False
    if not pin or (pin.status != "published" and not is_owner):
        # 404 rather than 403, so other people's drafts don't reveal that they exist.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pin not found")
    return pin


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
    current_user: User | None = Depends(get_current_user_optional),
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
        status = status or "published"  # public viewers only see published pins by default
    return pin_service.get_pins(db, owner_id=owner_id, status=status)


@router.get("/{pin_id}", response_model=PinDetail)
def get_pin(
    pin_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    pin = get_visible_pin(db, pin_id, current_user)

    return PinDetail(
        **PinOut.model_validate(pin).model_dump(exclude={"days_until_expiration"}),
        creator=PinUser.model_validate(pin.owner),
        like_count=pin_service.count_likes(db, pin_id),
        liked_by_me=(
            current_user is not None and pin_service.has_liked(db, pin_id, current_user.id)
        ),
    )


@router.post("/{pin_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def like_pin(
    pin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_visible_pin(db, pin_id, current_user)
    pin_service.like_pin(db, pin_id, current_user.id)


@router.delete("/{pin_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_pin(
    pin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_visible_pin(db, pin_id, current_user)
    pin_service.unlike_pin(db, pin_id, current_user.id)


@router.get("/{pin_id}/comments", response_model=list[CommentOut])
def list_comments(
    pin_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    get_visible_pin(db, pin_id, current_user)
    return pin_service.list_comments(db, pin_id)


@router.post(
    "/{pin_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    pin_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pin = get_visible_pin(db, pin_id, current_user)
    if not pin.allow_comments:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Comments are turned off for this pin")
    return pin_service.add_comment(db, pin_id, current_user.id, payload.body)