.PHONY: format lint test hooks check all

format:
	@echo "🧹 Running black and isort..."
	black --target-version py312 .
	isort .

lint:
	@echo "🔧 Running flake8..."
	flake8 .

test:
	@echo "🧪 Running pytest..."
	pytest tests/

hooks:
	@echo "⚙️ Installing pre-commit hooks..."
	pre-commit install

check:
	@echo "✅ Running pre-commit check..."
	pre-commit run --all-files

all: format lint test
