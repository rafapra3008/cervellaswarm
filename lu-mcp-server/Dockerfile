FROM python:3.12-slim

RUN useradd --system --no-create-home mcp

WORKDIR /app

COPY pyproject.toml README.md LICENSE lu_mcp_server.py ./

RUN pip install --no-cache-dir .

USER mcp

ENTRYPOINT ["lu-mcp-server"]
