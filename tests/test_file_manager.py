import pytest
import json
from pathlib import Path
from config.app_config import AppConfig
from core.file_manager import FileManager


@pytest.fixture(scope="session")
def config():
    return AppConfig()


@pytest.fixture(scope="session")
def file_manager(config):
    return FileManager(config)


@pytest.fixture
def tmp_text_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello, pytest!", encoding="utf-8")
    return file


@pytest.fixture
def tmp_json_file(tmp_path):
    file = tmp_path / "test.json"
    data = {"message": "Hello, JSON!"}
    file.write_text(json.dumps(data), encoding="utf-8")
    return file


def test_file_manager_text_load_save(file_manager, tmp_path):
    test_file = tmp_path / "sample.txt"
    test_data = "Test content"
    file_manager.save_file(test_data, "staging_data_dir", test_file.name)
    loaded_data = file_manager.load_file("staging_data_dir", test_file.name)
    assert isinstance(loaded_data, str)
    assert test_data in loaded_data


def test_file_manager_json_load_save(file_manager, tmp_path):
    test_file = tmp_path / "sample.json"
    test_data = {"key": "value"}
    file_manager.save_file(test_data, "staging_data_dir", test_file.name)
    loaded_data = file_manager.load_file("staging_data_dir", test_file.name)
    assert isinstance(loaded_data, dict)
    assert loaded_data.get("key") == "value"


def test_file_manager_overwrite_behavior(file_manager, tmp_path):
    test_file = tmp_path / "sample_overwrite.txt"
    initial_data = "Initial data"
    new_data = "New data"

    file_manager.save_file(initial_data, "staging_data_dir", test_file.name)
    with pytest.raises(FileExistsError):
        file_manager.save_file(new_data, "staging_data_dir", test_file.name, overwrite=False)

    file_manager.save_file(new_data, "staging_data_dir", test_file.name, overwrite=True)
    loaded_data = file_manager.load_file("staging_data_dir", test_file.name)
    assert new_data in loaded_data


def test_file_manager_unsupported_file(file_manager, tmp_path):
    test_file = tmp_path / "unsupported.xyz"
    with pytest.raises(ValueError):
        file_manager.save_file("data", "staging_data_dir", test_file.name)
