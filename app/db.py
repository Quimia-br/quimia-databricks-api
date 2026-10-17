import psycopg
from psycopg.rows import dict_row

from app import cache
from app.config import settings


def consultar(sql: str, params: dict | None = None) -> list[dict]:
    """Roda um SELECT no Postgres de serviço e devolve lista de dicts.

    Os parâmetros vão separados do SQL (%(nome)s), o que impede SQL injection.
    O resultado fica em cache pelo tempo de CACHE_TTL.
    """
    chave = (sql, str(sorted(params.items())) if params else "")
    cacheado = cache.get(chave)
    if cacheado is not None:
        return cacheado

    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        linhas = conn.execute(sql, params).fetchall()

    cache.set(chave, linhas, settings.cache_ttl)
    return linhas
