import json
import logging.config
import sys
from pathlib import Path


class AppConfig:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent
        self.config_path = self.base_dir / "settings.json"
        self._config = self._load_config()
        self._paths = self._setup_paths()

        # Init logger
        self._setup_logger()
        self.logger = logging.getLogger(self.app_name)

    def _load_config(self):
        """
        Load and parse the application's settings from settings.json.
        """
        if not self.config_path.is_file():
            sys.exit(FileNotFoundError(f"File '{self.config_path}' not found in project directory."))

        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _setup_paths(self):
        """
        Construct absolute paths for project directories defined in the config.
        """
        paths_dict = {}
        for dir_name, rel_path in self._config.get("paths", {}).items():
            paths_dict[dir_name] = self.base_dir / rel_path

        return paths_dict

    def _setup_logger(self):
        """
        Configure logging using the provided settings in the settings.json and ensure the logs directory exists.
        """
        logger_cfg = self._config.get("logging", {})
        default_logs = self.base_dir / "logs"
        logs_dir = self._paths.get("logs_dir", default_logs)
        logs_dir.mkdir(parents=True, exist_ok=True)  # <-- ensure logs directory exists, if not, create it

        logging.config.dictConfig(logger_cfg)

    @property
    def paths(self) -> dict[str, Path]:
        """
        Return dict of named absolute paths.
        """
        return self._paths

    @property
    def app_name(self):
        return self._config.get("app").get("name")

    @property
    def app_version(self):
        """
        Return app version from config, defaulting to '0.0.0'.
        """
        return self._config.get("app").get("version", "0.0.0")

    def get_path(self, dir_name: str):
        """
        Return absolute path for the given directory key.
        """
        if dir_name not in self._paths:
            sys.exit(KeyError(f"'{dir_name}' is not in configuration file!"))
        return self._paths[dir_name]
