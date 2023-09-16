FROM python:3.11

RUN apt-get update

WORKDIR /opt/app

ENV PYTHONPATH '/opt/app'

COPY pyproject.toml ./
COPY poetry.lock ./
RUN apt-get update \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY backend .

# CMD ["python", "-m", "bin"]