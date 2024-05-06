from fastapi import FastAPI

app = FastAPI(
    title="Weight tracker API",
    version="0.0.1",
    description="API for weight tracking and analysis",
    docs_url="/",
)
