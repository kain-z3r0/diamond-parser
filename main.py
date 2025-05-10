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
    
    # Define sample data to save as JSON
    filename = "e1.txt"
    
    
    # Load data file test
    data = file_manager.load_file("raw_data_dir", filename)
    logger.info("Loaded data: {data}")
    
    
    new_data = data + "NEW LINE!!!!! The Dodgers are losing!"
    
    # Save the data to output_data_dir
    file_manager.save_file(new_data, "staging_data_dir", filename)
    logger.info(f"Saved {filename} to staging_data_dir")
    
    
    # Print the loaded data to console
    print(new_data)

if __name__ == "__main__":
    main()