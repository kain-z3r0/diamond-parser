lint:
	pre-commit run --all-files || true

format:
	black .
	isort .

test:
	pytest

check:
	pre-commit run --all-files || true

install-hooks:
	pre-commit install
