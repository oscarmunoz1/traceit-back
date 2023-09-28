#!/usr/bin/env bash
# exit on error
set -o errexit
pip install --upgrade pip
pip install poetry

poetry env use 3.9

# Add this line to ensure Python 3.9 is in the PATH
export PATH=$HOME/.poetry/bin:$HOME/.poetry/envs/3.9/bin:$PATH

/opt/render/project/src/.venv/bin/poetry install
poetry install

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate