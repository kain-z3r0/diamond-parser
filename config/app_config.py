"""
AppConfig Module (app_config.py)

Provides the AppConfig class for centralized application configuration,
including loading settings, resolving project paths, and setting up logging.

Classes:
    AppConfig: Manages application settings, directory paths, and logging.

Example:
    from config.app_config import AppConfig

    config = AppConfig()
    paths = config.paths
    name = config.app_name
    version = config.app_version
    config.logger.info("Application started")

Dependencies:
    pathlib, logging, json, sys, pydantic
"""

from pathlib import Path
import logging.config
import json
from pydantic import BaseModel, ValidationError
from typing import Dict
import sys

__all__ = ["AppConfig"]  # Only expose AppConfig when using `from app_config import *`

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


class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when the settings.json file is missing."""
    pass  # Custom exception to allow specific catching of missing config file errors

class InvalidConfigKeyError(KeyError):
    """Raised when a requested config key does not exist."""
    pass  # Custom exception to handle missing keys in config cleanly


class AppMetadata(BaseModel):
    name: str
    version: str = "0.0.0"

class AppPaths(BaseModel):
    raw_data_dir: str
    output_data_dir: str
    staging_data_dir: str
    logs_dir: str

class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = True
    formatters: dict
    handlers: dict
    loggers: dict

class AppConfigSchema(BaseModel):
    app: AppMetadata
    paths: AppPaths
    logging: LoggingConfig


class AppConfig:
    """
    Central application configuration manager.

    Loads settings from a JSON file, validates with Pydantic models,
    constructs absolute directory paths, and sets up application logging.
    """

    def __init__(self):
        """
        Initialize AppConfig by loading settings, validating schema,
        setting up paths, and configuring logging.
        """
        self.base_dir = Path(__file__).resolve().parents[1]
        self.config_path = self.base_dir / "settings.json"
        
        # Load the config and validate it using the Pydantic model.
        self._config_data = self._load_config()

        # Build absolute paths from relative config values.
        self._resolved_paths = self._setup_paths()
        
        # Set up the application logger.
        self.logger = self._setup_logger()

    def _load_config(self) -> AppConfigSchema:
        """
        Load and parse settings from the settings.json file.

        Returns:
            AppConfigSchema: Parsed and validated configuration object.

        Raises:
            ConfigFileNotFoundError: If the settings.json file is missing.
            ValidationError: If the config structure is invalid.
        """
        if not self.config_path.is_file():
            # Raise a specific error instead of sys.exit() so caller can handle it.
            raise ConfigFileNotFoundError(
                f"File '{self.config_path}' not found in project directory."
            )

        with self.config_path.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)

        return AppConfigSchema(**raw_data)

    def _setup_paths(self) -> Dict[str, Path]:
        """
        Build absolute paths for project directories defined in the config.

        Returns:
            dict[str, Path]: Mapping of directory names to absolute Path objects.
        """
        # We resolve relative paths from config to absolute Path objects.
        resolved_paths = {}
        for field, rel_path in self._config_data.paths.model_dump().items():
            resolved_paths[field] = (self.base_dir / rel_path).resolve()
        return resolved_paths

    def _setup_logger(self) -> logging.Logger:
        """
        Configure logging based on the settings in the configuration file.

        Ensures the logs directory exists before setting up the logger.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logs_dir = self._resolved_paths.get("logs_dir")
        
        # Ensure the logs directory exists before setting up logging.
        logs_dir.mkdir(parents=True, exist_ok=True)

        logging.config.dictConfig(self._config_data.logging.model_dump())
        logger = logging.getLogger(self.app_name)
        logger.info("Logger initialized")
        return logger

    @property
    def paths(self) -> Dict[str, Path]:
        """
        Get the configured absolute directory paths.

        Returns:
            dict[str, Path]: Mapping of directory names to Path objects.
        """
        return self._resolved_paths

    @property
    def app_name(self) -> str:
        """
        Get the application name from the config.

        Returns:
            str: Application name.
        """
        return self._config_data.app.name

    @property
    def app_version(self) -> str:
        """
        Get the application version from the config.

        Returns:
            str: Application version, defaults to '0.0.0' if not set.
        """
        return self._config_data.app.version

    def get_path(self, dir_name: str) -> Path:
        """
        Retrieve the absolute path for a configured directory.

        Args:
            dir_name (str): Name of the directory as defined in the config.

        Returns:
            Path: Absolute Path object for the directory.

        Raises:
            TypeError: If dir_name is not a string.
            InvalidConfigKeyError: If the directory name is not found.
        """
        if not isinstance(dir_name, str):
            # Protect against invalid type inputs.
            raise TypeError("dir_name must be a string")

        if dir_name not in self._resolved_paths:
            # Raise a custom error to signal missing config key.
            raise InvalidConfigKeyError(f"'{dir_name}' is not in configuration file!")

        return self._resolved_paths[dir_name]
