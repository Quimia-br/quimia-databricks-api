from datetime import date

from fastapi import APIRouter, Depends, Query

from app.auth import verificar_chave
from app.db import consultar

# Todas as rotas exigem o header X-API-Key.
# Cada rota lê UMA tabela do schema gold. Não existe SQL livre vindo do cliente.
router = APIRouter(prefix="/v1", dependencies=[Depends(verificar_chave)])


# ---------- Usuários ----------

@router.get("/kpis/dau")
def dau(inicio: date | None = None, fim: date | None = None):
    """DAU por dia, com variação, média, desvio padrão e z-score."""
    return consultar(
        """
        SELECT * FROM gold.kpi_dau_diario
        WHERE (%(inicio)s::date IS NULL OR data >= %(inicio)s::date)
          AND (%(fim)s::date IS NULL OR data <= %(fim)s::date)
        ORDER BY data
        """,
        {"inicio": inicio, "fim": fim},
    )


@router.get("/usuarios/por-nivel-estado")
def usuarios_por_nivel_estado():
    """Usuários cadastrados por nível de acesso e estado."""
    return consultar(
        "SELECT * FROM gold.usuarios_por_nivel_estado ORDER BY nivel_acesso, estado"
    )


@router.get("/usuarios/engajamento")
def engajamento(
    nivel_acesso: str | None = None,
    estado: str | None = None,
    limite: int = Query(1000, ge=1, le=5000),
):
    """Sessões e dias ativos por usuário (uma linha por usuário)."""
    return consultar(
        """
        SELECT * FROM gold.engajamento_usuario
        WHERE (%(nivel)s::text IS NULL OR nivel_acesso = %(nivel)s::text)
          AND (%(estado)s::text IS NULL OR estado = %(estado)s::text)
        ORDER BY total_sessoes DESC
        LIMIT %(limite)s
        """,
        {"nivel": nivel_acesso, "estado": estado, "limite": limite},
    )


# ---------- Consultas e produtos ----------

@router.get("/kpis/recomendacoes")
def recomendacoes(inicio: date | None = None, fim: date | None = None):
    """Total de consultas e usuários distintos por dia."""
    return consultar(
        """
        SELECT * FROM gold.kpi_recomendacoes_diario
        WHERE (%(inicio)s::date IS NULL OR data >= %(inicio)s::date)
          AND (%(fim)s::date IS NULL OR data <= %(fim)s::date)
        ORDER BY data
        """,
        {"inicio": inicio, "fim": fim},
    )


@router.get("/produtos/top")
def produtos_top(limite: int = Query(10, ge=1, le=100)):
    """Produtos mais consultados, com ranking."""
    return consultar(
        "SELECT * FROM gold.kpi_top_produtos ORDER BY ranking, nome_produto LIMIT %(limite)s",
        {"limite": limite},
    )


# ---------- FDS ----------

@router.get("/fds/resolucao")
def fds_resolucao():
    """Percentual geral de substâncias resolvidas e pendentes."""
    return consultar("SELECT * FROM gold.kpi_resolucao_fds")


@router.get("/fds/distribuicao")
def fds_distribuicao():
    """Resolução por FDS, em nível de linha (boxplot)."""
    return consultar("SELECT * FROM gold.dist_resolucao_fds ORDER BY id_fds")


# ---------- Risco ----------

@router.get("/risco/cobertura")
def risco_cobertura():
    """Regras de incompatibilidade por classe química."""
    return consultar(
        "SELECT * FROM gold.kpi_cobertura_incompatibilidade ORDER BY pct_do_total DESC"
    )


# ---------- Estantes ----------

@router.get("/estantes/histograma")
def estantes_histograma():
    """Usuários por faixa de produtos organizados."""
    return consultar("SELECT * FROM gold.hist_produtos_por_estante ORDER BY faixa_inicio")


# ---------- Diagnóstico ----------

@router.get("/ping-db")
def ping_db():
    """Confirma que a API alcança o Postgres de serviço."""
    return consultar("SELECT 1 AS ok")
