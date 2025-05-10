## 📖 Pre-commit Workflow Guide

### ⚙️ Setup Instructions

1. Install Python project dependencies:
    ```bash
    pip install -r requirements.txt -r requirements-dev.txt
    ```

2. Install pre-commit hooks into git:
    ```bash
    pre-commit install
    ```

3. Run all pre-commit checks manually:
    ```bash
    make check
    ```

4. If pre-commit fixes files (like adding a newline), stage and commit:
    ```bash
    git add .
    git commit -m "Apply pre-commit auto-fixes"
    git push
    ```

5. If flake8 fails, check that `.pre-commit-config.yaml` has this line under flake8:
    ```yaml
    args: [--max-line-length=115, --extend-ignore=E203,W503]
    ```
    If missing, add it, then run:
    ```bash
    pre-commit clean
    pre-commit install
    ```
    and rerun:
    ```bash
    make check
    ```

---

### ✅ What’s configured in `.pre-commit-config.yaml`
- **black** → code formatting (115 chars)
- **flake8** → linting (115 chars, ignores E203, W503)
- **mypy** → type checking with explicit package bases
- **isort** → import sorting
- **bandit** → security scanning, skips tests/
- **end-of-file-fixer** → ensures final newline
- **trailing-whitespace** → trims extra whitespace

---

### 💡 Makefile Commands

| Command           | Description                              |
|-------------------|-----------------------------------------|
| make lint        | Run all pre-commit hooks                |
| make format      | Format code with black + isort          |
| make test        | Run pytest tests                        |
| make check       | Run pre-commit manually on all files    |
| make install-hooks | Install pre-commit hooks into git      |
| make clean       | Remove pycache, logs, temp files        |

---

## 🔧 Install Script (`install_dev.sh`)

```bash
#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial check
pre-commit run --all-files || true

# Reminder
echo "✅ Setup complete! Run 'make check' or commit changes."
```

Save this as `install_dev.sh`, then run:
```bash
bash install_dev.sh
```
