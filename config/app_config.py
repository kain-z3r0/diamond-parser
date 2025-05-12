"""
AppConfig Module

Provides centralized configuration management using a Singleton pattern,
Pydantic validation, and dynamic logging configuration for the application.
"""

import json
import logging.config
from pathlib import Path
from functools import lru_cache

from pydantic import BaseModel, BaseSettings

__all__ = ["get_app_config"]


# ----------------------------
# Custom Exceptions
# ----------------------------

class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when the settings.json file is missing."""
    pass


class InvalidConfigKeyError(KeyError):
    """Raised when a requested path key is not found in the config."""
    pass


# ----------------------------
# Pydantic Models
# ----------------------------

class AppMetadata(BaseModel):
    name: str
    version: str = "0.0.0"


class AppPaths(BaseModel):
    raw_data_dir: Path
    output_data_dir: Path
    staging_data_dir: Path
    logs_dir: Path


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = True
    formatters: dict
    handlers: dict
    loggers: dict


class AppConfigSchema(BaseSettings):
    app: AppMetadata
    paths: AppPaths
    logging: LoggingConfig

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ----------------------------
# AppConfig Singleton
# ----------------------------

class AppConfig:
    """
    Central app configuration loader and manager.

    Loads settings from JSON (and optionally .env), resolves paths,
    dynamically injects log file paths, configures logging, and provides
    access to application metadata and directories.
    """

    def __init__(self, config_file_path: Path | None = None):
        self.project_root = Path(__file__).resolve().parents[1]
        self.config_file_path = config_file_path or self.project_root / "settings.json"

        if not self.config_file_path.is_file():
            raise ConfigFileNotFoundError(f"Missing configuration file: {self.config_file_path}")

        self._config = self._load_config()
        self._absolute_paths = self._resolve_and_create_paths()
        self._inject_log_file_path()
        self.logger = self._configure_logging()

    def _load_config(self) -> AppConfigSchema:
        """Load and validate JSON-based config, allowing for .env overrides."""
        with self.config_file_path.open("r", encoding="utf-8") as file:
            raw_config = json.load(file)
        return AppConfigSchema(**raw_config)

    def _resolve_and_create_paths(self) -> dict[str, Path]:
        """
        Resolve relative paths to absolute paths from project root.

        Returns:
            dict[str, Path]: Resolved and auto-created directory paths.
        """
        resolved_paths = {}
        for key, val in self._config.paths.dict().items():
            path = Path(val).expanduser()
            if not path.is_absolute():
                path = (self.project_root / path).resolve()
            path.mkdir(parents=True, exist_ok=True)
            resolved_paths[key] = path
        return resolved_paths

    def _inject_log_file_path(self) -> None:
        """Inject resolved log file path into logging config before setup."""
        log_file = self._absolute_paths["logs_dir"] / "diamond_parser.log"
        handler = self._config.logging.handlers.get("file")
        if handler and "filename" in handler:
            handler["filename"] = str(log_file)

    def _configure_logging(self) -> logging.Logger:
        """Configure logging using the logging dictConfig."""
        logging.config.dictConfig(self._config.logging.dict())
        logger = logging.getLogger(self.app_name)
        logger.info("Logger initialized.")
        return logger

    @property
    def paths(self) -> dict[str, Path]:
        return self._absolute_paths

    @property
    def app_name(self) -> str:
        return self._config.app.name

    @property
    def app_version(self) -> str:
        return self._config.app.version

    def get_path(self, config_key: str) -> Path:
        """
        Retrieve an absolute path for a config key.

        Args:
            config_key (str): The directory key from the settings.

        Returns:
            Path: Resolved absolute path.

        Raises:
            InvalidConfigKeyError: If key is not defined in the config.
        """
        if not isinstance(config_key, str):
            raise TypeError("config_key must be a string")
        if config_key not in self._absolute_paths:
            raise InvalidConfigKeyError(f"Invalid path key: '{config_key}'")
        return self._absolute_paths[config_key]


# ----------------------------
# Singleton Accessor
# ----------------------------

@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    """
    Returns the singleton instance of AppConfig.

    Ensures config is loaded only once during app lifetime.
    """
    return AppConfig()



# ----------------------------
# Explanation of important design choices
# ----------------------------

# __all__ = ["AppConfig"]
# This defines the public API of the module.
# When someone does `from app_config import *`,
# only the names listed in __all__ will be imported.
# This prevents internal helpers or exceptions from leaking into the namespace.
# It also signals that AppConfig is the main intended public class.

# class ConfigFileNotFoundError(FileNotFoundError):
# This is a custom exception that inherits from Python’s built-in FileNotFoundError.
# It is raised when the settings.json file is missing.
# The benefit of using a custom exception is that downstream code can
# catch this specific error without catching all FileNotFoundError cases.
# Example:
# try:
#     config = AppConfig()
# except ConfigFileNotFoundError:
#     handle_missing_config()

# class InvalidConfigKeyError(KeyError):
# This is a custom exception that inherits from Python’s built-in KeyError.
# It is raised when a requested directory name or config key does not exist.
# Using a custom exception makes it easy to handle this exact failure
# without interfering with other KeyError cases.
# Example:
# try:
#     path = config.get_path("nonexistent_dir")
# except InvalidConfigKeyError:
#     handle_missing_directory()