# Diamond Parser

A Python application for parsing and managing baseball data.

## 📦 Features

- Load and save JSON and text files using handler classes.
- Automatic formatting, linting, type checking, and security checks.
- Pre-commit integration for clean and safe commits.
- Simple Makefile for running common tasks.

---

## ⚙ Setup

1. Clone the repository:
    git clone <repo-url>
    cd diamond-parser

2. Create a virtual environment:
    python -m venv .venv
    source .venv/bin/activate  # on Linux/macOS
    .venv\Scripts\activate     # on Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Install pre-commit hooks:
    pre-commit install

---

## ✅ Workflow

1. Make code changes.
2. Run all checks:
    make check
3. Format code:
    make format
4. Run tests:
    make test
5. Commit your changes:
    git add .
    git commit -m "Describe your change"
    git push

Pre-commit will run automatically on every commit.

---

## 💡 Makefile Commands

| Command           | Description                              |
|-------------------|-----------------------------------------|
| make lint        | Run all pre-commit hooks                |
| make format      | Format code with black + isort          |
| make test        | Run pytest tests                        |
| make check       | Run pre-commit manually on all files    |
| make install-hooks | Install pre-commit hooks into git      |

---

## 🔥 Notes

- The `archive/` directory is **excluded** from all tools.
- `mypy` is configured to ignore missing stubs like `pydantic` and `pytest`.
- `bandit` skips the `tests/` folder to avoid false positives on `assert`.

---

## 📂 Project Structure

.
├── Makefile
├── README.md
├── pyproject.toml
├── .pre-commit-config.yaml
├── .mypy.ini
├── config/
├── core/
├── parser/
├── pipeline/
├── tests/
├── archive/  # excluded from checks
└── data/

---

## ✨ Contributing

1. Fork this repo.
2. Create a new branch.
3. Submit a pull request with your changes.

---

## 📄 License

MIT License © Your Name
