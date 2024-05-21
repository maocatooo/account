import datetime
from collections.abc import Generator
import uuid

from app.core.db import engine, SessionDep
from typing import Sequence
from sqlmodel import Session, select, update, delete
from app.model import User
from app.model import Tag
from app.model import ID
from app.model import BookJournal
from app.model import SaveTag
from sqlalchemy.exc import NoResultFound


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def upsert_user(session: SessionDep, u_info: User) -> User:
    try:
        u = session.exec(select(User).where(User.openid == u_info.openid)).one()
        u.avatar = u_info.avatar
        u.username = u_info.username
        u.last_time = datetime.datetime.now()
        session.add(u)
        session.commit()
        return u
    except NoResultFound:
        pass
    u_info.id = str(uuid.uuid4().hex)
    u_info.last_time = datetime.datetime.now()
    session.add(u_info)
    session.commit()
    return u_info


def tags(session: SessionDep, user_id: str) -> Sequence[Tag]:
    ts = session.exec(select(Tag).where(Tag.uid == user_id)).all()
    return ts


def create_tag(session: SessionDep, user_id: str, s: SaveTag):
    tag = Tag()
    tag.id = str(uuid.uuid4().hex)
    tag.name = s.name
    tag.icon = s.icon
    tag.uid = user_id
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def update_tag(session: SessionDep, user_id: str, s: SaveTag):
    stmt = update(Tag).values(name=s.name, icon=s.icon)
    session.exec(stmt)
    session.commit()
    return s


def delete_tag(session: SessionDep, user_id: str, s: SaveTag):
    stmt = delete(Tag).where(Tag.id == s.id, Tag.uid == user_id)
    session.exec(stmt)
    session.commit()
    return s


def create_book_journals(session: SessionDep, user_id: str, b: BookJournal) -> BookJournal:
    b.id = str(uuid.uuid4().hex)
    b.uid = user_id
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


def update_book_journals(session: SessionDep, user_id: str, b: BookJournal) -> BookJournal:
    stmt = update(BookJournal).where(BookJournal.id == b.id, BookJournal.uid == user_id).values(**b.dict())
    session.exec(stmt)
    session.commit()
    return b


def delete_book_journals(session: SessionDep, user_id: str, s: ID):
    stmt = delete(BookJournal).where(BookJournal.id == s.id, BookJournal.uid == user_id)
    session.exec(stmt)
    session.commit()
    return s
