from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from src.utils.db_utils import close_db
from src.modules.auth.router import router as auth_router
from src.modules.weight.router import router as weight_router
from src.config import cors_config


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="Weight tracker API",
    version="0.0.1",
    summary="Weight tracker API",
    description="API for weight tracking and analysis",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    weight_router,
    prefix="/weight",
    tags=["Weight tracking"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=cors_config.CORS_METHODS,
    allow_headers=cors_config.CORS_HEADERS,
)