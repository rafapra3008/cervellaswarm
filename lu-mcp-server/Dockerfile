FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE lu_mcp_server.py ./

RUN pip install --no-cache-dir .

ENTRYPOINT ["lu-mcp-server"]
