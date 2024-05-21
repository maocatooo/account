from sqlmodel import Session, create_engine

from typing import Annotated
from collections.abc import Generator
from fastapi import Depends
from app.core.config import settings

engine = create_engine(settings.MySQLDSN)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
