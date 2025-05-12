# **app\_config.py — Centralized Configuration Management**

This module serves as the centralized hub for configuration management, handling settings loading,
directory resolution, and logger setup for the entire application.

---

## **🔧 Purpose**

This script is the **centralized configuration hub** for the project, with the following responsibilities:

* **Loads structured settings** from `settings.json` using Pydantic for validation.
* **Supports environment variable overrides** via a `.env` file for flexible configuration.
* **Resolves and creates** all necessary directories based on the configuration.
* **Configures logging** using Python's logging system with a dynamic configuration.
* **Exposes application metadata** like name, version, and provides access to resolved paths.

---

## **🧱 Design Patterns**

### **1. Singleton Pattern (via `@lru_cache`)**

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    return AppConfig()
```

* **Ensures** that only **one instance** of `AppConfig` is created and used throughout the
  application, preventing multiple initializations.
* **Avoids** accidental re-loading of the configuration or creation of duplicate logger instances,
  which could lead to inconsistent states.
* **Leverages** Python's `functools.lru_cache` for a simple, efficient, and thread-safe implementation
  of the singleton pattern.

### **2. Configuration Pattern**

* **Utilizes** `pydantic.BaseSettings` to define and manage settings with strong type validation and
  support for environment variables.
* **Facilitates** easy expansion for future configuration needs, such as adding secrets, API keys,
  or database connection strings.

---

## **📦 Technologies Used**

* **Pydantic**: For parsing and validating the JSON configuration with type safety.
* **Logging Config Dict**: Dynamically configures the logging system, including injecting the log file
  path for the `RotatingFileHandler`.
* **Pathlib**: Handles path resolution and ensures all necessary directories are created safely.

---

## **📂 How It Works**

1. **Configuration Schema**

   * **`AppConfigSchema`**: A Pydantic model that defines the structure and types expected in
     `settings.json`.

2. **Initialization**

   * **In `AppConfig.__init__`**:

     * **Loads** settings from `settings.json` and applies any overrides from a `.env` file.
     * **Resolves** all relative paths based on the project's root directory.
     * **Creates** any missing directories specified in the configuration.
     * **Dynamically injects** the log file path (`logs_dir/diamond_parser.log`) into the logging
       configuration.
     * **Applies** the logging configuration to set up the application's logging system.

3. **Accessing the Configuration**

   * **Use `get_app_config()`** to retrieve the singleton instance of `AppConfig` from anywhere in
     the application.
   * **Access resolved directory paths** using `config.get_path("raw_data_dir")`, where
     `"raw_data_dir"` is a key defined in the configuration.

---

## **✨ Benefits for Production**

* **Efficiency**: Initializes only once, making it safe for use in CLI tools, servers, or test suites.
* **Flexibility**: Supports configuration from both JSON and environment variables.
* **Reliability**: Provides type-safe and validated configuration settings.
* **Automation**: Automatically creates necessary directories and logs startup information.
* **Extensibility**: Easily accommodates additional settings like database configurations or
  credentials.

---

## **🧪 Example Usage**

```python
from config.app_config import get_app_config

config = get_app_config()
print(config.app_name)
print(config.get_path("output_data_dir"))
config.logger.info("App started.")
```

---

## **🚀 Next Steps**

With the configuration system in place, you can now focus on building other critical components, such as:

* **File Management**: Implement handlers for managing files and directories.
* **Database Connections**: Add settings and logic for database interactions.
* **CLI Overrides**: Enhance flexibility with command-line argument parsing or additional
  environment variable support.

---

You now have a **professional-grade configuration engine** ready for real-world applications,
educational purposes, or to showcase in job interviews.

**Would you like assistance in elevating your `file_manager.py` to the same standard of quality?**

---

### **Key Improvements Made**

1. **Clarity**: Rephrased sections for better readability and precision (e.g., title, purpose, how it
   works).
2. **Consistency**: Standardized formatting and terminology across sections (e.g., bolding key
   terms, aligning bullet styles).
3. **Professionalism**: Enhanced explanations with more context (e.g., why the singleton pattern is
   beneficial) and polished the tone.
4. **Code Formatting**: Fixed the example usage code block to be properly indented and
   self-contained.
5. **Structure**: Kept the original layout intact while making it more concise and impactful where
   appropriate.
