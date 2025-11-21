from fastapi import FastAPI
from .api.ingest_controller import router as ingest_router

app = FastAPI(title="Agnostic Data Agent")

app.include_router(ingest_router, prefix="/api", tags=["ingest"])
