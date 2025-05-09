from pathlib import Path
import json
import logging.config
from typing import Any, Dict

class AppConfig:
    """
    Load settings from JSON, ensure dirs exist, configure logging,
    and expose app metadata and paths.
    """
    def __init__(self) -> None:
        # Base directory is the directory containing this file
        self.base_dir: Path = Path(__file__).resolve().parent
        self.config_path: Path = self.base_dir / "settings.json"

        self._config: Dict[str, Any] = self._load_config()
        self._paths: Dict[str, Path] = self._setup_paths()

        self._setup_logging()
        self.logger = logging.getLogger(self.app_name)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file using json.load for efficiency."""
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _setup_paths(self) -> Dict[str, Path]:
        paths: Dict[str, Path] = {}
        for name, rel_path in self._config.get("paths", {}).items():
            path = self.base_dir / rel_path
            path.mkdir(parents=True, exist_ok=True)
            paths[name] = path
        return paths

    def _setup_logging(self) -> None:
        log_cfg = self._config.get("logging", {})
        default_logs = self.base_dir / "logs"
        logs_dir = self._paths.get("logs_dir", default_logs)
        logs_dir.mkdir(parents=True, exist_ok=True)

        logging.config.dictConfig(log_cfg)

    @property
    def app_name(self) -> str:
        return self._config.get("app", {}).get("name", "app")

    @property
    def app_version(self) -> str:
        return self._config.get("app", {}).get("version", "0.0.0")

    @property
    def paths(self) -> Dict[str, Path]:
        return self._paths

    def get_path(self, name: str) -> Path:
        if name not in self._paths:
            raise KeyError(f"No path named '{name}' in configuration")
        return self._paths[name]


def main():
    # 1. Instantiate — this auto-creates dirs and sets up logging
    cfg = AppConfig()

    # 2. Print project base_dir
    print("Project base_dir:", cfg.base_dir)

    # 3. Print every configured path
    print("\nConfigured paths:")
    for name, path in cfg.paths.items():
        print(f"  {name:20s} → {path}")

    # 4. Emit logs at all levels
    log = cfg.logger
    log.debug(   "DEBUG    → only to file (verbose formatter).")
    log.info(    "INFO     → to stderr (simple formatter).")
    log.warning( "WARNING  → stderr + file.")
    log.error(   "ERROR    → stderr + file.")
    log.critical("CRITICAL → stderr + file.")

if __name__ == "__main__":
    main()
