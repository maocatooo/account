from fastapi import APIRouter
from app.curd import SessionDep
from sqlmodel import select
from app.model import Book
from app.api.deps import CurrentUser

router = APIRouter()


@router.get("/book")
def books(db:SessionDep, current_user: CurrentUser ) :
    ts = db.exec(select(Book).where(Book.uid == current_user.id)).all()
    return ts
