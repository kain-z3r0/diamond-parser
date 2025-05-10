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

    def load_file(self, filename: str | Path) -> str | dict[str, Any]:
        filepath = self._to_path(filename)
        handler = self._get_handler(filepath)
        return handler.load(filepath)

    def save_file(self, data: str | dict[str, Any], filename: str | Path) -> None:
        filepath = self._to_path(filename)
        handler = self._get_handler(filepath)
        handler.save(data, filepath)

    def load_from_config(self, dir_key: str, filename: str) -> str | dict[str, Any]:
        base_dir = self.config.get_path(dir_key)
        return self.load_file(base_dir / filename)

    def save_to_config(
        self, data: str | dict[str, Any], dir_key: str, filename: str
    ) -> None:
        base_dir = self.config.get_path(dir_key)
        self.save_file(data, base_dir / filename)
