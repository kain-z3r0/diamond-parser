import logging
from config.app_config import AppConfig
from core.fm_wip import FileManager

def main():
    # Initialize AppConfig to load settings and configure logger
    config = AppConfig()
    
    # Access the logger from AppConfig
    logger = config.logger
    logger.info("Application started.")
    
    # Initialize FileManager with the AppConfig instance
    file_manager = FileManager(config)
    
    # Define sample data to save as JSON
    data = {"key": "value", "number": 42}
    output_dir_key = "output_data_dir"
    filename = "example.json"
    
    # Save the data to output_data_dir
    file_manager.save_to_config(data, output_dir_key, filename)
    logger.info(f"Saved {filename} to {output_dir_key}")
    
    # Load the data back and log it
    loaded_data = file_manager.load_from_config(output_dir_key, filename)
    logger.info(f"Loaded data: {loaded_data}")
    
    # Print the loaded data to console
    print(loaded_data)

if __name__ == "__main__":
    main()