[private]
default:
    @just --list

# Builds mypyc wheels locally
build:
    uv pip uninstall crossandra 2> /dev/null
    rm -rf build
    python setup.py install

# Installs the project
install:
    uv venv
    uv pip install . -r dev-requirements.txt

# Runs pytest, mypy, ruff
check:
    python -m pytest --cov crossandra --cov-report term-missing
    mypy --strict crossandra tests
    ruff check
    ruff format --check
