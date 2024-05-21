from app.model import LoginWeChat, Token
from app.core import security
from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from app.curd import SessionDep, upsert_user
from app.model import User
from app.core.security import get_openid
from app.api.deps import CurrentUser

router = APIRouter()


@router.post("/login")
def login_wechat(db:SessionDep, req: LoginWeChat ) -> Token:
    openid = get_openid(req.code)
    user = User(
        openid=openid,
        username=req.name,
        avatar_url=req.avatar_url,
    )
    user = upsert_user(db, user)
    access_token_expires = timedelta(days=3)
    return Token(
        id=user.id,
        name=user.username,
        avatar_url=user.avatar,
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.get("/users/me")
async def read_users_me(current_user: CurrentUser):
    return current_user
