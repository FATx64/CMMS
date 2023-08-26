FROM python:3.10.9-slim as base

LABEL org.opencontainers.image.source="https://github.com/FATx64/CMMS"
LABEL org.opencontainers.image.description="A reliable scheduling, tracking, reporting tools for equipment and facilities maintenance"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

ENV PATH="/venv/bin:/root/.local/bin:${PATH}" \
    VIRTUAL_ENV="/venv"

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        bash \
        brotli \
        build-essential \
        curl \
        gettext \
        git \
        libpq-dev \
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    && python -m venv /venv

ENV NVM_DIR=/usr/local/nvm
ENV NODE_VERSION=18.17.0

RUN mkdir $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# ---
FROM base as builder

WORKDIR /app

ENV DJANGO_STATIC="/app/public"

COPY poetry.lock pyproject.toml scripts.py manage.py ./
RUN poetry install --no-root --no-directory
ADD cmms/ ./cmms
RUN poetry install --without dev
RUN poetry run manage tailwind install
RUN poetry run manage tailwind build
RUN poetry run manage collectstatic --noinput

# ---
FROM base as final

WORKDIR /app

COPY --from=builder /venv /venv
COPY --from=builder /app/pyproject.toml /app/
COPY --from=builder /app/manage.py /app/
COPY --from=builder /app/cmms/ /app/cmms

EXPOSE 8000

CMD [ "gunicorn", "cmms.core.asgi:application", "-k", "uvicorn.workers.UvicornWorker" ]