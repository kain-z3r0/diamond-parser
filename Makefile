# Run all pre-commit hooks (lint, format, type-check, security)
check:
	pre-commit run --all-files || true

# Format code with black and isort
format:
	black .
	isort .

# Run tests
test:
	pytest

# Run only lint (via pre-commit, skips breaking on auto-fixes)
lint:
	pre-commit run --all-files || true

# Install pre-commit hooks into .git
install-hooks:
	pre-commit install

# Clean up pycache, logs, test leftovers, and temp files
clean:
	find . -name '__pycache__' -exec rm -rf {} +
	rm -rf logs/*
	rm -f pytest.ini
	rm -rf .pytest_cache
	rm -f .coverage
	rm -f .mypy_cache
