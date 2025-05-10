lint:
	pre-commit run --all-files

test:
	pytest

format:
	black .
	isort .
