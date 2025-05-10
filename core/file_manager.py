"""
FileManager Module
==================

Provides functionality for loading and saving files using various handlers.
It includes a `FileHandler` protocol with concrete implementations for JSON and
text files, and a `FileManager` class that handles the correct file type based on
file extension.

Components:
-----------
- `FileHandler` protocol: Defines `load(filepath)` and `save(data, filepath)` methods.
- `JSONFileHandler`: Implements JSON file handling using the `json` module.
- `TextFileHandler`: Handles plain text files using the `pathlib` module.
- `FileManager`: Manages file operations, choosing the correct handler based on file extension.

Usage:
------
```python
from config.app_config import AppConfig
from file_manager import FileManager

config = AppConfig()
fm = FileManager(config)

# Load a JSON file from the 'data_dir' path:
data = fm.load_file('data_dir', 'data.json')

# Save a text file to the 'logs_dir' path:
fm.save_file("Hello, world!", 'logs_dir', 'notes.txt')


Dependencies:
-------------
    - json
    - pathlib
    - typing
    - config.app_config.AppConfig
"""

import json
from pathlib import Path
from typing import Protocol, Type, ClassVar, Any

from config.app_config import AppConfig


class FileHandler(Protocol):
    @classmethod
    def load(cls, filepath: Path) -> str | dict[str, Any]: ...
    @classmethod
    def save(cls, data: str | dict[str, Any], filepath: Path) -> None: ...


class JSONFileHandler:
    @classmethod
    def load(cls, filepath: Path) -> dict[str, Any]:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save(cls, data: dict[str, Any], filepath: Path) -> None:
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


class TextFileHandler:
    @classmethod
    def load(cls, filepath: Path) -> str:
        return filepath.read_text(encoding="utf-8")

    @classmethod
    def save(cls, data: str, filepath: Path) -> None:
        filepath.write_text(data, encoding="utf-8")


class FileManager:
    _handlers: ClassVar[dict[str, Type[FileHandler]]] = {
        ".json": JSONFileHandler,
        ".txt": TextFileHandler,
    }

    def __init__(self, config: AppConfig):
        self.config = config

    def _to_path(self, filename: str | Path) -> Path:
        return filename if isinstance(filename, Path) else Path(filename)

    def _get_handler(self, filepath: Path) -> Type[FileHandler]:
        ext = filepath.suffix.lower()
        handler = self._handlers.get(ext)
        if not handler:
            supported = ", ".join(self._handlers.keys())
            raise ValueError(f"Unsupported file type: {ext!r}. Supported: {supported}")
        return handler

    def load_file(self, dir_key: str, filename: str) -> str | dict[str, Any]:
        base_dir = self.config.get_path(dir_key)
        filepath = base_dir / filename
        handler = self._get_handler(filepath)
        return handler.load(filepath)

    def save_file(self, data: str | dict[str, Any], dir_key: str, filename: str) -> None:
        base_dir = self.config.get_path(dir_key)
        filepath = base_dir / filename
        handler = self._get_handler(filepath)
        handler.save(data, filepath)
