[private]
default:
    @just --list

install:
    uv venv
    uv pip install . -r dev-requirements.txt

check:
    python -m pytest --cov crossandra --cov-report term-missing
    mypy --strict crossandra tests
    ruff check
    ruff format --check
