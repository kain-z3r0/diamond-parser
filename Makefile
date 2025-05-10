lint:
	pre-commit run --all-files

format:
	black .
	isort .

test:
	pytest

check:
	pre-commit run --all-files

install-hooks:
	pre-commit install
