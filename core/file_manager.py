"""
FileManager Module

Provides file loading and saving capabilities using handler classes
for different file types (e.g., JSON, text), with logging and
overwrite control.

Classes:
    FileHandler: Protocol defining load/save interface.
    JSONFileHandler: Handles reading/writing JSON files.
    TextFileHandler: Handles reading/writing text files.
    FileManager: Manages file operations, selecting the appropriate handler,
                 with logging and error handling.

Example:
    from config.app_config import AppConfig
    from file_manager import FileManager

    config = AppConfig()
    fm = FileManager(config)

    # Load JSON file
    data = fm.load_file('data_dir', 'data.json')

    # Save text file
    fm.save_file("Hello, world!", 'logs_dir', 'notes.txt')

Dependencies:
    json, pathlib, typing, config.app_config.AppConfig
"""

import json
from pathlib import Path
from typing import Protocol, Type, ClassVar, Any

from config.app_config import AppConfig


class FileHandler(Protocol):
    """
    Protocol for file handlers.
    Defines a common interface for loading and saving files.
    """
    @classmethod
    def load(cls, filepath: Path) -> str | dict[str, Any]: ...
    
    @classmethod
    def save(cls, data: str | dict[str, Any], filepath: Path) -> None: ...


class JSONFileHandler:
    """
    Handler for reading and writing JSON files.
    """
    @classmethod
    def load(cls, filepath: Path) -> dict[str, Any]:
        """
        Load JSON data from a file.

        Args:
            filepath (Path): Path to the JSON file.

        Returns:
            dict[str, Any]: Parsed JSON data.
        """
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save(cls, data: dict[str, Any], filepath: Path) -> None:
        """
        Save data as JSON to a file.

        Args:
            data (dict[str, Any]): Data to save.
            filepath (Path): Path to the JSON file.
        """
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


class TextFileHandler:
    """
    Handler for reading and writing text files.
    """
    @classmethod
    def load(cls, filepath: Path) -> str:
        """
        Load text content from a file.

        Args:
            filepath (Path): Path to the text file.

        Returns:
            str: File content as a string.
        """
        return filepath.read_text(encoding="utf-8")

    @classmethod
    def save(cls, data: str, filepath: Path) -> None:
        """
        Save text content to a file.

        Args:
            data (str): Text data to save.
            filepath (Path): Path to the text file.
        """
        filepath.write_text(data, encoding="utf-8")


class FileManager:
    """
    Manager for loading and saving files with appropriate handlers.
    Supports logging and overwrite control.
    """
    _handlers: ClassVar[dict[str, Type[FileHandler]]] = {
        ".json": JSONFileHandler,
        ".txt": TextFileHandler,
    }

    def __init__(self, config: AppConfig):
        """
        Initialize FileManager with an AppConfig instance.

        Args:
            config (AppConfig): Application configuration.
        """
        self.config = config
        self.logger = config.logger  # Use AppConfig logger for logging

    def _to_path(self, filename: str | Path) -> Path:
        """
        Convert a string or Path to a Path object.

        Args:
            filename (str | Path): Filename or Path.

        Returns:
            Path: Path object.
        """
        return filename if isinstance(filename, Path) else Path(filename)

    def _get_handler(self, filepath: Path) -> Type[FileHandler]:
        """
        Get the handler class for a file based on its extension.

        Args:
            filepath (Path): File path.

        Returns:
            Type[FileHandler]: Corresponding file handler class.

        Raises:
            ValueError: If the file extension is unsupported.
        """
        ext = filepath.suffix.lower()
        handler = self._handlers.get(ext)
        if not handler:
            supported = ", ".join(self._handlers.keys())
            raise ValueError(f"Unsupported file type: {ext!r}. Supported: {supported}")
        return handler

    def load_file(self, dir_key: str, filename: str) -> str | dict[str, Any]:
        """
        Load a file from a directory specified by the config.

        Args:
            dir_key (str): Directory key from the config.
            filename (str): Filename to load.

        Returns:
            str | dict[str, Any]: Loaded file data.

        Raises:
            IOError: If the file cannot be loaded.
        """
        base_dir = self.config.get_path(dir_key)
        filepath = base_dir / filename
        handler = self._get_handler(filepath)
        try:
            data = handler.load(filepath)
            self.logger.info(f"Loaded file: {filepath}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to load file {filepath}: {e}")
            raise IOError(f"Failed to load {filepath}: {e}") from e

    def save_file(
        self,
        data: str | dict[str, Any],
        dir_key: str,
        filename: str,
        overwrite: bool = True
    ) -> None:
        """
        Save data to a file in a directory specified by the config.

        Args:
            data (str | dict[str, Any]): Data to save.
            dir_key (str): Directory key from the config.
            filename (str): Filename to save.
            overwrite (bool): Whether to overwrite if the file exists.

        Raises:
            FileExistsError: If overwrite is False and file exists.
            IOError: If the file cannot be saved.
        """
        base_dir = self.config.get_path(dir_key)
        filepath = base_dir / filename

        if filepath.exists() and not overwrite:
            self.logger.warning(f"File exists and overwrite is False: {filepath}")
            raise FileExistsError(f"{filepath} already exists and overwrite is False.")

        handler = self._get_handler(filepath)
        try:
            handler.save(data, filepath)
            self.logger.info(f"Saved file: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save file {filepath}: {e}")
            raise IOError(f"Failed to save {filepath}: {e}") from e
