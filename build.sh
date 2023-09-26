#!/usr/bin/env bash
# exit on error
set -o errexit
pip install --upgrade pip
pip install poetry
/opt/render/project/src/.venv/bin/poetry install
poetry install

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate