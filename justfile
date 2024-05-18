[private]
default:
    @just --list

install:
    uv venv
    uv pip install . -r dev-requirements.txt

check:
    python -m pytest
    mypy --strict crossandra tests
    ruff check
    ruff format --check
