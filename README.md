# bevaring-cli

CLI tool to work with bevaring.

## Project prerequisites

- [`python >= 3.10`](https://www.python.org/downloads/)
- [`pipx`](https://pypa.github.io/pipx/installation/)

### Development prerequisites

- [`poetry`](https://python-poetry.org/docs/)

## Installation

Before installing `bevaring-cli`, make sure you have the [prerequisites](#project-prerequisites) installed.

```shell
pipx install https://github.com/arkivverket/bevaring-cli/releases/download/0.1.0/bevaring_cli-0.1.0-py3-none-any.whl
```

## Usage

See [`USAGE.md`](USAGE.md)

## Usage (development)

Enter the poetry environment (`poetry shell`), are pre-prend all commands with `poetry run`.

```shell
python -m bevaring_cli.main [OPTIONS] COMMAND [ARGS]...
```

**Example**:

```shell
python -m bevaring_cli.main login
python -m bevaring_cli.main --endpoint bevaring.test.digitalarkivet.no login
```

### Building wheel

```shell
poetry build --format wheel
```
