import secrets

from fastapi import Header, HTTPException

from app.config import settings


def verificar_chave(x_api_key: str | None = Header(default=None)):
    # Sem o header ou com chave errada, a resposta é sempre 401.
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status_code=401, detail="chave inválida")
