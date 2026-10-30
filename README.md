# TESTES_PRATICOS_SQL_XSS_API

Laboratório prático de segurança ofensiva e defensiva aplicado a uma **API de catálogo de filmes**, construída com FastAPI + SQLite + Pytest.

O projeto demonstra, por meio de testes automatizados, vulnerabilidades de **SQL Injection (OWASP A03)** e **Cross-Site Scripting (XSS)** em endpoints de login e comentários de filmes, comparando versões intencionalmente vulneráveis com versões seguras refatoradas.

## Tecnologias

- Python 3.11+
- FastAPI + Uvicorn
- SQLite (em memória)
- Pytest + HTTPX
- uv (gerenciador de ambiente)

## Como executar

```bash
uv init TESTES_PRATICOS_SQL_XSS_API
cd TESTES_PRATICOS_SQL_XSS_API
uv add fastapi uvicorn pytest httpx pydantic
uv run pytest -v