from fastapi import APIRouter
from app.curd import SessionDep
from sqlmodel import func, select
from app.model import Tag
from app.model import SaveTag
from app.core.security import get_openid
from app.api.deps import CurrentUser
from app.curd import SessionDep
from app.api.deps import abort_error
from app.curd import create_tag, update_tag, delete_tag

router = APIRouter()


@router.get("/tag")
def tags(db: SessionDep, current_user: CurrentUser):
    ts = db.exec(select(Tag).where(Tag.uid == current_user.id)).all()
    return ts


@router.post("/tag")
def tags(db: SessionDep, current_user: CurrentUser, req: SaveTag):
    if req.name.strip() == "":
        abort_error()
    ts = db.exec(select(Tag).where(Tag.uid == current_user.id, Tag.name == req.name)).all()
    if ts:
        abort_error()
    return create_tag(db, current_user.id, req)


@router.put("/tag")
def tags(db: SessionDep, current_user: CurrentUser, req: SaveTag):
    if req.name.strip() == "":
        return abort_error()
    ts = db.exec(select(Tag).where(Tag.uid == current_user.id, Tag.name == req.name, Tag.id != req.id)).all()
    if ts:
        abort_error()
    return update_tag(db, current_user.id, req)


@router.delete("/tag")
def tags(db: SessionDep, current_user: CurrentUser, req: SaveTag):
    if req.id.strip() == "":
        return abort_error()
    return delete_tag(db, current_user.id, req)
