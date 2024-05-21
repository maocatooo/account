from fastapi import APIRouter

from app.api.routes import login,book,tag,journal

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(book.router, tags=["book"])
api_router.include_router(tag.router, tags=["tag"])
api_router.include_router(journal.router, tags=["journal"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])