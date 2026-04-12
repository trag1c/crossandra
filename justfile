[private]
default:
    @just --list

# Runs pytest, mypy, ruff
check:
    uv run pytest -vv
    uv run mypy --strict src tests
    uv run ruff check
    uv run ruff format --check

# Runs ruff's formatter and ruff's isort rules
format:
    uv run ruff format
    uv run ruff check --select I,RUF022,RUF023 --fix

# Runs ruff in fix mode
fix:
    uv run ruff check --fix
