from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db 
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.board import BoardCreate, BoardUpdate, BoardOut
from app.services import board_service

router = APIRouter(prefix="/boards", tags=["boards"])

@router.post("", response_model=BoardOut)
def create_board(
    payload: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return board_service.create_board(db, owner_id=current_user.id, payload=payload)

@router.get("", response_model=list[BoardOut])
def list_boards(
    mine: bool = False,
    username: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    boards = board_service.get_boards(db, owner_id=owner_id)

    # public viewers never see someone else's secret boards
    if username and (not current_user or current_user.id != owner_id):
        boards = [b for b in boards if not b.is_secret]

    return boards

@router.get("/{board_id}", response_model=BoardOut)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = board_service.get_board(db, board_id)
    if not board:
        raise HTTPException(404, "Board not found")
    return board

@router.patch("/{board_id}", response_model=BoardOut)
def update_board(
    board_id: int,
    payload: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board = board_service.update_board(db, board_id, owner_id=current_user.id, payload=payload)
    if not board:
        raise HTTPException(404, "Board not found")
    return board

@router.delete("/{board_id}", status_code=204)
def delete_board(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = board_service.delete_board(db, board_id, owner_id=current_user.id)
    if not deleted:
        raise HTTPException(404, "Board not found")