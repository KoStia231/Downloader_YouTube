#!/bin/bash

PROJECT_PATH=$(dirname "$(realpath "$0")")

VENV_PATH="$PROJECT_PATH/.venv/bin/activate"
MAIN_FILE="main.py"


echo "Запуск main.py..."

cd "$PROJECT_PATH" || exit

source "$VENV_PATH"

python "$MAIN_FILE"
deactivate
