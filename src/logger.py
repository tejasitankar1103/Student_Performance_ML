import logging  # Python's built-in module to create and manage log messages
import os       # For handling file and directory operations
from datetime import datetime  # To get current time and date

## This file sets up a logger to log messages to a file with a timestamp in its name.

# Create a log file name using the current date and time
# Example output: "06-09-2025_13_45_22.log"
# This ensures that each time the program runs, it creates a uniquely named log file
LOG_FILE = f"{datetime.now().strftime('%m-%d-%Y_%H_%M_%S')}.log"

# Get the full path where logs should be stored.
# os.getcwd() gets the current working directory of your project.
# This line will create a path like: "current_folder/logs/06-09-2025_13_45_22.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) 

# Create the logs folder if it doesn’t already exist.
# os.makedirs creates all folders in the path if needed.
# exist_ok=True avoids error if the folder already exists.
os.makedirs(logs_path, exist_ok=True)  

# Define the full path for the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Setting up the logger with basic configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Save logs to the generated file
    level=logging.INFO,      # Minimum level of logs to record: DEBUG < INFO < WARNING < ERROR < CRITICAL
                             # INFO means it will log info, warning, error, critical, but not debug by default.
    
    # Format of each log message
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    # Explanation of format parts:
    # %(asctime)s  → shows the time the log was created
    # %(lineno)d   → line number in the code where the log was generated
    # %(name)s     → name of the logger (default will be "root" unless customized)
    # %(levelname)s → the log level (INFO, ERROR, etc.)
    # %(message)s  → the actual log message you write
)
