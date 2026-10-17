# quimia-api

API de consulta aos KPIs do Quimia. Lê o schema `gold` de um Postgres de serviço, que o Job do Databricks atualiza a cada execução, e devolve JSON para a aplicação web.

```
Databricks (gold) -> Job -> Postgres de serviço (schema gold) -> quimia-api (Render) -> app web
```

## Estrutura

```
quimia-api/
├── app/
│   ├── __init__.py
│   ├── main.py      # app FastAPI, CORS e /health
│   ├── config.py    # variáveis de ambiente
│   ├── auth.py      # chave de API (header X-API-Key)
│   ├── cache.py     # cache em memória com validade
│   ├── db.py        # conexão com o Postgres
│   └── routes.py    # endpoints (um por tabela gold)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | String do Postgres de serviço, com `?sslmode=require`. Use usuário somente leitura. |
| `API_KEY` | Chave que a aplicação web envia no header `X-API-Key`. |
| `CACHE_TTL` | Validade do cache em segundos (padrão 3600). |
| `CORS_ORIGINS` | Origens permitidas, separadas por vírgula. |

## Rodar localmente

```bash
pip install -r requirements.txt
cp .env.example .env        # preencha
uvicorn app.main:app --reload
```

Documentação interativa: http://localhost:8000/docs

## Endpoints (prefixo `/v1`, todos com `X-API-Key`)

| Rota | Tabela gold | Filtros |
|---|---|---|
| `GET /kpis/dau` | `kpi_dau_diario` | `inicio`, `fim` |
| `GET /kpis/recomendacoes` | `kpi_recomendacoes_diario` | `inicio`, `fim` |
| `GET /produtos/top` | `kpi_top_produtos` | `limite` |
| `GET /fds/resolucao` | `kpi_resolucao_fds` | |
| `GET /fds/distribuicao` | `dist_resolucao_fds` | |
| `GET /risco/cobertura` | `kpi_cobertura_incompatibilidade` | |
| `GET /estantes/histograma` | `hist_produtos_por_estante` | |
| `GET /usuarios/por-nivel-estado` | `usuarios_por_nivel_estado` | |
| `GET /usuarios/engajamento` | `engajamento_usuario` | `nivel_acesso`, `estado`, `limite` |
| `GET /ping-db` | | diagnóstico |

`GET /health` não exige chave e não acessa o banco.

## Deploy no Render

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`
- Variáveis: `DATABASE_URL`, `API_KEY`, `CACHE_TTL`, `CORS_ORIGINS`, `PYTHON_VERSION`

## Contrato com a gold

A API depende dos nomes das tabelas e colunas do schema `gold`. Se o pipeline mudar uma tabela, atualize a rota correspondente.
