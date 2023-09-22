FROM python:3.11

RUN mkdir --parents /opt/app
COPY pyproject.toml /opt/app/pyproject.toml
COPY poetry.lock /opt/app/poetry.lock
COPY poetry.toml /opt/app/poetry.toml

WORKDIR /opt/app

RUN pip install poetry \    
    && poetry install --no-dev

COPY bin /opt/app/bin
COPY lib /opt/app/lib
COPY entrypoint.sh /opt/app/entrypoint.sh

RUN chmod +x /opt/app/entrypoint.sh
