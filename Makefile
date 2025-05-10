# Makefile for diamond-parser project

.PHONY: format lint test hooks all

format:
	@echo "🛠 Running black and isort..."
	black .
	isort .

lint:
	@echo "🔍 Running flake8..."
	flake8 .

test:
	@echo "✅ Running pytest..."
	pytest tests/

hooks:
	@echo "⚙️  Installing pre-commit hooks..."
	pre-commit install

all: format lint test
