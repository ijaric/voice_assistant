FROM python:3.11

WORKDIR /opt/app

ENV PYTHONPATH '/opt/app'

COPY pyproject.toml ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY backend/bin bin
COPY backend/libs libs
COPY entrypoint.sh .
RUN chmod +x /opt/app/entrypoint.sh
