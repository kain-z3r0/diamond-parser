"""
AppConfig Module

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
    pathlib, logging, json, sys
"""

from pathlib import Path
import logging.config
import json
import sys


class AppConfig:
    """
    Central application configuration manager.

    Loads settings from a JSON file, constructs absolute directory paths,
    and sets up application logging.
    """

    def __init__(self):
        """
        Initialize AppConfig by loading settings, setting up paths, and configuring logging.
        """
        self.base_dir = Path(__file__).resolve().parents[1]
        self.config_path = self.base_dir / "settings.json"
        self._config = self._load_config()
        self._paths = self._setup_paths()
        self.logger = self._setup_logger()

    def _load_config(self):
        """
        Load and parse settings from the settings.json file.

        Exits the program if the file is not found.

        Returns:
            dict: Parsed configuration data.
        """
        if not self.config_path.is_file():
            sys.exit(
                FileNotFoundError(
                    f"File '{self.config_path}' not found in project directory."
                )
            )
        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _setup_paths(self):
        """
        Build absolute paths for project directories defined in the config.

        Returns:
            dict[str, Path]: Mapping of directory names to absolute Path objects.
        """
        paths_dict = {}
        for dir_name, rel_path in self._config.get("paths", {}).items():
            paths_dict[dir_name] = self.base_dir / rel_path
        return paths_dict

    def _setup_logger(self):
        """
        Configure logging based on the settings in the configuration file.

        Ensures the logs directory exists before setting up the logger.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger_cfg = self._config.get("logging", {})
        default_logs = self.base_dir / "logs"
        logs_dir = self._paths.get("logs_dir", default_logs)
        logs_dir.mkdir(parents=True, exist_ok=True)

        logging.config.dictConfig(logger_cfg)
        logger = logging.getLogger(self.app_name)
        print(f"Logger setup: {logger}")
        return logger

    @property
    def paths(self) -> dict[str, Path]:
        """
        Get the configured absolute directory paths.

        Returns:
            dict[str, Path]: Mapping of directory names to Path objects.
        """
        return self._paths

    @property
    def app_name(self) -> str:
        """
        Get the application name from the config.

        Returns:
            str: Application name.
        """
        return self._config.get("app", {}).get("name")

    @property
    def app_version(self) -> str:
        """
        Get the application version from the config.

        Returns:
            str: Application version, defaults to '0.0.0' if not set.
        """
        return self._config.get("app", {}).get("version", "0.0.0")

    def get_path(self, dir_name: str) -> Path:
        """
        Retrieve the absolute path for a configured directory.

        Args:
            dir_name (str): Name of the directory as defined in the config.

        Returns:
            Path: Absolute Path object for the directory.

        Raises:
            SystemExit: If the directory name is not found in the config.
        """
        if dir_name not in self._paths:
            sys.exit(KeyError(f"'{dir_name}' is not in configuration file!"))
        return self._paths[dir_name]
