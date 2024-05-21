from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime


class LoginWeChat(BaseModel):
    code: str | None = None
    avatar_url: str | None = None
    name: str | None = None


class Token(BaseModel):
    id: str | None = None
    name: str | None = None
    access_token: str | None = None
    avatar_url: str | None = None


class SaveTag(BaseModel):
    id: str = ""
    name: str = ""
    icon: str = ""


class SaveBookJournal(BaseModel):
    book_id: str = ""
    date: str = ""


class ID(BaseModel):
    id: str = ""


class AsrJournal(BaseModel):
    book_id: str
    describe: str


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    username: str = ""
    email: str = ""
    password_hash: str = ""
    openid: str = ""
    last_time: datetime = ""
    avatar: str = ""

    class Config:
        # 使用 exclude 参数指定要忽略的字段
        json_exclude = {'last_time', "password_hash", "openid"}


class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    icon: str
    uid: str


class Book(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    tp: int = 0
    uid: str


class BookJournal(SQLModel, table=True):
    __tablename__ = "book_journal"
    id: str = Field(primary_key=True)
    tid: str = ""
    tname: str = ""
    name: str = ""
    date: str = ""
    amount: str = ""
    record: str = ""
    book_id: str = ""
    uid: str = ""


