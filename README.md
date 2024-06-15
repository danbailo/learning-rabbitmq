# Learning RabbitMQ

Repository dedicated to study and learning somethings about RabbitMQ.

## Make
The project uses a [Makefile](Makefile) to facilitate project installation, lint execution, typing and testing.

### Preparing virtual enviroment

It is highly recommended to use virtual environments when developing Python projects.

### Using poetry

Install [poetry](https://github.com/python-poetry/poetry) then install the project using Make.

```
make install
```

### Using pyenv

Install the [prerequisites](https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites) and then install [pyenv](https://github.com/pyenv/pyenv-installer). After install and configure pyenv, just install the project using Make.

```
make install_with_pyenv
```

### Checkers

`make check_format` - Checks code formatting.

`make format` - Automatically formats the code.

`make check_lint` - Checks the code lint.

`make lint` - Formats the code by automatically correcting the lint.

`make check_types` - Checks the typing hinting of the code.

`make check_all` - Runs all the project's "checkers" and tests signaling when everything is ok. This way, it is certain that the pull-request pipeline will be ready to go to main.

All settings defined in formatting, typing, lint, etc. They are defined in the Python project configuration file - [pyproject.toml](pyproject.toml).

## Docker

Prepare the RabbitMQ container running this commands

1. Build image
```
docker compose build
```

2. Then run container

```
docker compose up -d
```

## Running project

To run the project, just open a terminal and run the project as a module. Example:

```bash
python -m learning_rabbitmq.samples.dead_letter_exchange.consumer
```

```bash
python -m learning_rabbitmq.samples.dead_letter_exchange.producer
```
