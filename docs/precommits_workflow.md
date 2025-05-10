# Pre-commit Workflow Guide

This guide explains the workflow for using pre-commit, linting, formatting, and testing in this project.

---

## 1. Setup (run once per machine)

    pip install pre-commit
    pre-commit install
    pre-commit run --all-files

---

## 2. Typical development workflow

1. Write or modify code.

2. Run lint and tests:

    make lint
    make test

3. Format the code:

    make format

4. Stage and commit clean files:

    git add .
    git commit -m "Describe your change"
    git push

---

## 3. Optional: Run pre-commit manually

    pre-commit run --all-files

---

## Summary of Makefile commands

| Command      | Description                |
|-------------|---------------------------|
| make lint   | Runs all pre-commit hooks |
| make test   | Runs pytest tests         |
| make format | Runs black + isort        |

---

## Notes

- `.pre-commit-config.yaml` → defines the hooks
- `.flake8` → sets linting rules
- `pyproject.toml` → configures black, isort, and other tools
