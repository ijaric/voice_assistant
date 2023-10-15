#!/bin/bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do sleep 1; done;

poetry run alembic upgrade head

exec .venv/bin/python -m bin
