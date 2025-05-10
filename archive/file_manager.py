import app_config

from pathlib import Path
import csv
import json

import pandas as pd d

from typing import Any, Protocol, ClassVar, Type

class FileHandler(Protocol):
    @classmethod
    def load(cls, path: Path) -> dict | str | list[dict[str, str]]: ...
    
    @classmethod
    def save(cls, data: dict | str | list[dict[str, Any]], path: Path) -> None: ...

class JSONFileHandler:
    @classmethod
    def load(cls, path: Path) -> dict:
        return json.load(path.open("r", encoding="utf-8"))

    @classmethod
    def save(cls, data: dict, path: Path) -> None:
        path.open("w", encoding="utf-8").write(json.dumps(data, indent=2))

class TextFileHandler:
    @classmethod
    def load(cls, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    @classmethod
    def save(cls, data: str, path: Path) -> None:
        path.write_text(data, encoding="utf-8")

class CSVFileHandler:
    @classmethod
    def load(cls, path: Path) -> list[dict[str, str]]:
        with path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    @classmethod
    def save(cls, data: list[dict[str, Any]], path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

class FileManager:
    _handlers: ClassVar[dict[str, Type[FileHandler]]] = {
        ".json": JSONFileHandler,
        ".txt": TextFileHandler,
        ".log": TextFileHandler,
        ".md": TextFileHandler,
        ".csv": CSVFileHandler,
    }

    def _to_path(self, path: str | Path) -> Path:
        return Path(path) if isinstance(path, str) else path

    def _get_handler(self, path: Path) -> Type[FileHandler]:
        ext = path.suffix.lower()
        handler = self._handlers.get(ext)
        if not handler:
            supported = ", ".join(self._handlers.keys())
            raise ValueError(
                f"Unsupported file type: {ext!r}. Supported: {supported}"
            )
        return handler

    def load_file(self, path: str | Path) -> Any:
        p = self._to_path(path)
        return self._get_handler(p).load(p)

    def save_file(self, data: Any, path: str | Path) -> None:
        p = self._to_path(path)
        self._get_handler(p).save(data, p)

    @classmethod
    def register_handler(cls, extension: str, handler: Type[FileHandler]) -> None:
        if not extension.startswith("."):
            extension = "." + extension
        cls._handlers[extension.lower()] = handler

# Register pandas-based CSV handler unconditionally
class PandasCSVHandler:
    @classmethod
    def load(cls, path: Path) -> pd.DataFrame:
        return pd.read_csv(path, encoding="utf-8")

    @classmethod
    def save(cls, data: pd.DataFrame, path: Path) -> None:
        data.to_csv(path, index=False, encoding="utf-8")

FileManager.register_handler(".csv", PandasCSVHandler)


def main() -> None:
    fm = FileManager()

    # JSON
    cfg = fm.load_file("config.json")
    cfg["added"] = 1
    fm.save_file(cfg, "config_out.json")

    # Text
    txt = fm.load_file("example.md")
    fm.save_file(txt + "\n# Extra\n", "example_out.md")

    # CSV via pandas
    df = fm.load_file("data.csv")       # returns DataFrame
    print(df.head())
    fm.save_file(df, "data_out.csv")

if __name__ == "__main__":
    main()
