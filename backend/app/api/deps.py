from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings
from typing import Annotated, List, Sequence
from collections.abc import Generator
from fastapi import Depends, HTTPException, status
from app.model import User
from app.core.db import  SessionDep

ALGORITHM = "HS256"

oauth2_scheme = HTTPBearer()

async def get_current_user(db: SessionDep, token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    print(token)
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return db.get(User, payload.get("user_id"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


CurrentUser = Annotated[User, Depends(get_current_user)]


err = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="HTTP_400_BAD_REQUEST",
)

def abort_error():
    raise err