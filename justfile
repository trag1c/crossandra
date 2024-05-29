[private]
default:
    @just --list

build:
    uv pip uninstall crossandra 2> /dev/null
    rm -rf build
    python setup.py install

install:
    uv venv
    uv pip install . -r dev-requirements.txt

check:
    python -m pytest --cov crossandra --cov-report term-missing
    mypy --strict crossandra tests
    ruff check
    ruff format --check
