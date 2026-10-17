from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import router

app = FastAPI(title="Quimia API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_lista,
    allow_methods=["GET"],
    allow_headers=["X-API-Key"],
)

app.include_router(router)


@app.get("/health")
def health():
    # Sem autenticação e sem tocar no banco: serve ao health check do Render.
    return {"status": "ok"}
