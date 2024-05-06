from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.utils.db_utils import close_db
from src.modules.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Weight tracker API",
    version="0.0.1",
    description="API for weight tracking and analysis",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)
