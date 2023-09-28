set -o errexit
pip install --upgrade pip
pip install poetry

# Ensure the virtual environment is activated
source /opt/render/project/src/.venv/bin/activate

poetry env use 3.9

# Install dependencies using Poetry
poetry install

# Run your Django management commands
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate