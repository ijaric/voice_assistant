FROM ghcr.io/yp-middle-python-24/python-dev:3.10-jammy-0.0.1 AS builder

RUN mkdir --parents /opt/app
COPY pyproject.toml /opt/app/pyproject.toml
COPY poetry.lock /opt/app/poetry.lock
COPY poetry.toml /opt/app/poetry.toml

WORKDIR /opt/app
RUN poetry install --no-dev

FROM ghcr.io/yp-middle-python-24/python:3.10-jammy-0.0.1 AS runtime

RUN mkdir --parents /opt/app
COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY bin /opt/app/bin
COPY lib /opt/app/lib

WORKDIR /opt/app
CMD [".venv/bin/python", "-m", "bin.main"]
