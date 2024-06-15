REPOSITORY = learning-rabbitmq
SOURCE = learning_rabbitmq

install:
	@echo "\nInstalling project..."
	@poetry install --no-root
	@echo "\nProject installed!"

check_format:
	@poetry run ruff format $(SOURCE) --check

format:
	@poetry run ruff format $(SOURCE)

check_lint:
	@poetry run ruff check $(SOURCE)

lint:
	@poetry run ruff check $(SOURCE) --fix

check_types:
	@poetry run mypy $(SOURCE)

check_all: check_format check_lint check_types
	@echo "\nAll checks have been passed!"

prepare_env_pyenv:
	@echo "\nPreparing virtualenv using pyenv..."
	@pyenv update
	@pyenv install 3.11.3 -s
	@pyenv virtualenv -f 3.11.3 learning_rabbitmq-env
	@pyenv local learning_rabbitmq-env

	@echo "\nInstalling poetry..."
	@pip install poetry
	@poetry config virtualenvs.create false --local
	@poetry config virtualenvs.prefer-active-python true --local

	@echo "\nProject prepared to install!"

install_with_pyenv: prepare_env_pyenv install
	@echo "\nProject installed with pyenv!"