from sqlalchemy.orm import Session
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


def create_board(db: Session, owner_id: int, payload: BoardCreate) -> Board:
    board = Board(owner_id=owner_id, **payload.model_dump())
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def update_board(db: Session, board_id: int, owner_id: int, payload: BoardUpdate) -> Board | None:
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == owner_id).first()
    if not board:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(board, field, value)
    db.commit()
    db.refresh(board)
    return board


def get_boards(db: Session, owner_id: int | None = None) -> list[Board]:
    query = db.query(Board)
    if owner_id is not None:
        query = query.filter(Board.owner_id == owner_id)
    return query.order_by(Board.created_at.desc()).all()


def get_board(db: Session, board_id: int) -> Board | None:
    return db.query(Board).filter(Board.id == board_id).first()


def delete_board(db: Session, board_id: int, owner_id: int) -> bool:
    board = db.query(Board).filter(Board.id == board_id, Board.owner_id == owner_id).first()
    if not board:
        return False
    db.delete(board)
    db.commit()
    return True