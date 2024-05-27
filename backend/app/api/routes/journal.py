from fastapi import APIRouter
from app.curd import SessionDep, create_book_journals, update_book_journals, delete_book_journals
from sqlmodel import select, func, text
from app.model import BookJournal, ID, AsrJournal
from app.api.deps import CurrentUser
from datetime import datetime
from app.core.security import qcloud_asr_generate_url
from app.core.journal import asr_to_journal

router = APIRouter()


@router.get("/journal")
def journals(db: SessionDep, current_user: CurrentUser, date="", book_id=""):
    current_date = datetime.strptime(date, "%Y-%m")
    next_date = datetime(current_date.year, current_date.month + 1, day=1)
    ts = db.exec(select(BookJournal).where(
        BookJournal.uid == current_user.id, BookJournal.book_id == book_id,
        BookJournal.date >= current_date, BookJournal.date <= next_date)
                 .order_by(text("date DESC"))).all()
    return ts


@router.post("/journal")
def journals(db: SessionDep, current_user: CurrentUser, req: BookJournal):
    return create_book_journals(db, current_user.id, req)


@router.put("/journal")
def journals(db: SessionDep, current_user: CurrentUser, req: BookJournal):
    return update_book_journals(db, current_user.id, req)


@router.delete("/journal")
def journals(db: SessionDep, current_user: CurrentUser, req: ID):
    return delete_book_journals(db, current_user.id, req)


@router.get("/name_prompt")
def name_prompt(db: SessionDep, current_user: CurrentUser, tid=""):
    stmt = select(BookJournal.name, func.count(None).label("c")) \
        .where(BookJournal.tid == tid, BookJournal.uid == current_user.id) \
        .group_by(BookJournal.name) \
        .order_by(text("c DESC")).limit(10)
    res = db.exec(
        stmt
    ).all()
    return [i[0] for i in res]


@router.post("/qcloudAsrGenerateUrl")
def asr_generate_url(db: SessionDep, current_user: CurrentUser):
    return {
        "url": qcloud_asr_generate_url()
    }


@router.post("/journal_by_asr")
def asr_generate_url(db: SessionDep, current_user: CurrentUser, req: AsrJournal):
    return asr_to_journal(db, current_user, req)
