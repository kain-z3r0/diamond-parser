from pathlib import Path

import pytest

from config.app_config import AppConfig, InvalidConfigKeyError


@pytest.fixture(scope="session")
def config():
    return AppConfig()


def test_app_config_load(config):
    assert config.app_name == "diamond-parser"
    assert config.app_version == "0.1.0"
    assert "logs_dir" in config.paths


def test_app_config_get_path(config):
    path = config.get_path("logs_dir")
    assert isinstance(path, Path)
    assert path.exists() or not path.exists()  # We just check it's a Path


def test_app_config_invalid_key(config):
    with pytest.raises(InvalidConfigKeyError):
        config.get_path("nonexistent_dir")
