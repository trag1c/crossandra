[private]
default:
    @just --list

install:
    uv venv
    uv pip install . -r dev-requirements.txt

check:
    pytest
    mypy --strict crossandra
    mypy tests
    ruff check
    ruff format --check
