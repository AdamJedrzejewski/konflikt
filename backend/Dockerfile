# Backend OBSIL. Budowanie z katalogu głównego repozytorium:
#   docker build -f backend/Dockerfile .
# Codex CLI (połączenie z modelem przez subskrypcję ChatGPT). Wersja sprawdzona z aplikacją.
FROM node:22-slim AS codex
ARG CODEX_VERSION=0.156.1
RUN npm install -g @openai/codex@${CODEX_VERSION} && npm cache clean --force

FROM python:3.12-slim
COPY --from=codex /usr/local/bin/node /usr/local/bin/node
COPY --from=codex /usr/local/lib/node_modules/@openai/codex /usr/local/lib/node_modules/@openai/codex
RUN ln -s /usr/local/lib/node_modules/@openai/codex/bin/codex.js /usr/local/bin/codex

WORKDIR /srv/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /srv/backend/
COPY rules/ /srv/rules/

# Logowanie Codexa trzymane na trwałym wolumenie, nie w obrazie.
ENV CODEX_HOME=/data/codex \
    KNOWLEDGE_PROJECT_PATH=/knowledge \
    PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 1000 obsil && mkdir -p /data/codex && chown -R obsil /data
USER obsil

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
