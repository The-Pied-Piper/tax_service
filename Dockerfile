# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.txt ./

# --- dev: runtime + tooling + generator deps; source is bind-mounted by compose --
FROM base AS dev
# gh comes from GitHub's own apt repo; Debian's package lags well behind.
ADD --chmod=644 https://cli.github.com/packages/githubcli-archive-keyring.gpg /etc/apt/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
        > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends git gh openssh-client \
    && rm -rf /var/lib/apt/lists/*
# Pin GitHub's SSH host keys system-wide (HOME=/tmp, so ~/.ssh/known_hosts
# wouldn't survive a rebuild). Taken from the TLS-authenticated meta API rather
# than ssh-keyscan, so there's no trust-on-first-use.
RUN python -c "import json,urllib.request; \
keys=json.load(urllib.request.urlopen('https://api.github.com/meta'))['ssh_keys']; \
open('/etc/ssh/ssh_known_hosts','w').write(''.join(f'github.com {k}\n' for k in keys))"
# compose.yaml runs as the host's UID:GID; ssh looks up the home dir via
# getpwuid() and refuses to run ("No user exists for uid") without an entry.
ARG UID=1000 GID=1000
RUN (getent group "$GID" || groupadd -g "$GID" dev) \
    && useradd -o -u "$UID" -g "$GID" -d /tmp -M -s /bin/bash dev
COPY requirements-dev.txt ./
COPY tools/service_gen/requirements.txt tools/service_gen/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements-dev.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# --- prod: runtime deps only, source baked in, non-root -------------------------
FROM base AS prod
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
RUN useradd --system --no-create-home --shell /usr/sbin/nologin app
COPY openapi ./openapi
COPY alembic.ini ./
COPY migrations ./migrations
COPY data ./data
COPY app ./app
USER app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
