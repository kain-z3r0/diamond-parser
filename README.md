# Diamond Parser

A Python application for parsing and managing baseball data.

---

## 🚀 Project Features

- Centralized configuration management with `AppConfig`
- File loading and saving with `FileManager` for JSON and text files
- Pre-commit hooks for code quality: Black, Flake8, isort
- Automated tests with pytest
- Customizable project paths via `settings.json`

---

## 📦 Project Structure

```
/diamond-parser
    /config             → AppConfig module
    /core               → FileManager module
    /tests              → pytest test files
        /fixtures       → test data files (optional)
    .gitignore          → ignored files/folders
    .pre-commit-config.yaml → pre-commit hooks setup
    Makefile           → common dev tasks (format, lint, test)
    pyproject.toml    → tool configs (Black, Flake8, isort)
    README.md         → this file
    requirements.txt  → (optional) dependency list
    settings.json     → app-level config (paths, logging)
```

---

## ⚙️ Setup Instructions

1️⃣ **Clone the repository**

```bash
git clone <your-repo-url>
cd diamond-parser
```

2️⃣ **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

3️⃣ **Install dependencies**

```bash
pip install -r requirements.txt
```

4️⃣ **Install pre-commit hooks**

```bash
pre-commit install
```

---

## 🔥 Usage

```bash
python main.py
```

This will:
- Load `settings.json`
- Initialize logging
- Run sample file operations with `FileManager`

---

## 🧪 Run Tests

```bash
pytest tests/
```

---

## 🛠 Developer Commands (Makefile)

| Command           | Description                          |
|-------------------|-------------------------------------|
| `make format`    | Run Black + isort                  |
| `make lint`      | Run Flake8 linting                |
| `make test`      | Run pytest tests                  |
| `make hooks`     | Install pre-commit hooks         |
| `make all`       | Run format, lint, and test       |

---

## 📄 Configuration

- `settings.json`: runtime config (app name, version, paths, logging)
- `.pre-commit-config.yaml`: git hook configs (Black, Flake8, isort)
- `pyproject.toml`: tool configs (line length, versions, exclusions)

---

## ✨ Future Improvements (ideas)

- Add CSV/YAML file handlers
- Add CLI interface
- Add Dockerfile for deployment
- Add CI pipeline with GitHub Actions

---

## 📄 License

MIT License
