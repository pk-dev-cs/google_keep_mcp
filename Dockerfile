FROM python:3.11-slim

ENV UV_PYTHON_DOWNLOADS=never
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

WORKDIR /app
RUN python -m pip install --no-cache-dir uv==0.13.6

COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/
COPY scripts/get_master_token.py ./scripts/get_master_token.py
RUN uv sync --locked --no-dev --no-editable

RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

CMD ["python", "-m", "google_keep_mcp.server", "--transport", "stdio"]
