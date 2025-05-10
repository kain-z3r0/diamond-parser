import logging
from config.app_config import AppConfig
from core.file_manager import FileManager


def main():
    # Initialize AppConfig to load settings and configure logger
    config = AppConfig()

    # Access the logger from AppConfig
    logger = config.logger
    logger.info("Application started.")

    # Initialize FileManager with the AppConfig instance
    file_manager = FileManager(config)

    # Define sample file and directory
    filename = "e1.txt"
    dir_key_load = "raw_data_dir"
    dir_key_save = "staging_data_dir"

    try:
        # Load data file test
        data = file_manager.load_file(dir_key_load, filename)
        logger.info(f"Loaded data from {dir_key_load}/{filename}: {data}")
    except Exception as e:
        logger.error(f"Failed to load file: {e}")
        return

    # Modify the loaded data
    new_data = data + "\nNEW LINE!!!!! The Dodgers are losing!"

    try:
        # Test saving with overwrite = False (will raise if file exists)
        file_manager.save_file(new_data, dir_key_save, filename, overwrite=False)
        logger.info(f"Saved {filename} to {dir_key_save} (overwrite=False)")
    except FileExistsError as e:
        logger.warning(f"File already exists, trying again with overwrite=True: {e}")
        # Now save with overwrite = True
        try:
            file_manager.save_file(new_data, dir_key_save, filename, overwrite=True)
            logger.info(f"Saved {filename} to {dir_key_save} (overwrite=True)")
        except Exception as e:
            logger.error(f"Failed to save file even with overwrite=True: {e}")
            return

    # Print the modified data to console
    print(f"Final data saved:\n{new_data}")


if __name__ == "__main__":
    main()
