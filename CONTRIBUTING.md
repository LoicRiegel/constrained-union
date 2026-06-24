# Contributing

## Tests and code quality tools

The following tools are used:
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [mypy](https://www.mypy-lang.org/index.html) for type checking (or [ty](https://docs.astral.sh/ty/) for experimentation)
- [prek](https://prek.j178.dev/) (or [pre-commit](https://pre-commit.com/)) for pre-commit hooks
- [pytest](https://docs.pytest.org/) for testing
- [tox](https://tox.wiki/) for isolated test/lint environments

## Local setup

Install development dependencies:
```sh
uv sync --group dev
```

Install pre-commit hooks (only once per clone):
```sh
uv run prek install
```

Run the code quality checks with:
```sh
uv run prek run --all-files
```

Run the linter with:
```sh
uv run ruff check --fix
```

Run the formatter with:
```sh
uv run ruff format
```

Run the type checker with:
```sh
uv run mypy .
```

Run tests and lint checks against all supported python versions with tox:
```sh
uv run tox
```
