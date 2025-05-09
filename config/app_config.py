import json
import logging
import logging.config
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    app: dict = field(default_factory=dict)
    paths: dict[str, str] = field(default_factory=dict)
    logging_cfg: dict = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Path = Path("settings.json")) -> "AppConfig":
        if not config_path.is_file():
            raise FileNotFoundError(f"{config_path} not found.")
        data = json.loads(config_path.read_text())

        # Ensure paths exist
        for p in data.get("paths", {}).values():
            Path(p).mkdir(parents=True, exist_ok=True)

        # Configure logging
        log_cfg = data.get("logging", {})
        if log_cfg:
            logging.config.dictConfig(log_cfg)

        return cls(
            app=data.get("app", {}),
            paths=data.get("paths", {}),
            logging_cfg=log_cfg
        )

    def get_config(self, section: str, key: str = None):
        sec = getattr(self, section, {})
        return sec[key] if key else sec

    def get_logger(self) -> logging.Logger:
        return logging.getLogger("diamond_parser")


if __name__ == "__main__":
    cfg = AppConfig.load()
    logger = cfg.get_logger()

    # This will go into the file only
    logger.debug("Debugging details")

    # These will appear on console (stderr) and in the file
    logger.warning("This is a warning")
    logger.error("This is an error")

    print("App name:", cfg.get_config("app", "name"))
    print("Raw data dir:", cfg.get_config("paths", "raw_data_dir"))
