# Contributing

## Tests and code quality tools

The following tools are used:
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [mypy](https://www.mypy-lang.org/index.html) for type checking (or [ty](https://docs.astral.sh/ty/) for experimentation)
- [prek](https://prek.j178.dev/) (or [pre-commit](https://pre-commit.com/)) for pre-commit hooks
- [pytest](https://docs.pytest.org/) for testing

Run the code quality checks with:
```sh
uv run prek install  # only once
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
