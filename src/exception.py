import sys  # Importing the sys module to access system-specific functions and exceptions
from src.logger import logging  # Importing the custom logger setup from logger.py

## This file contains custom exception classes and a function to handle error messages.

## Function to format error messages with details
def error_message_detail(error, error_detail: sys):
    # This function is used to create a detailed error message 
    # It helps track the file name, line number, and the actual error message
    # This makes debugging easier when errors occur

    ## first and second details provided are not used 
    ## only third detail is used it provides the traceback information
    ##like file name, line number, etc.
    _, _, exc_tb = error_detail.exc_info()  # Getting traceback object from exception info

    ## Extracting the file name and line number from the traceback
    file_name = exc_tb.tb_frame.f_code.co_filename  # Getting the name of the file where the error occurred
    line_number = exc_tb.tb_lineno  # Getting the exact line number where the error happened

    # Formatting the error message with file name, line number, and error message
    # This creates a user-friendly and informative message for logging or displaying
    error_message = "Error occurred in python script name [{0}] at line number [{1}] with message [{2}]".format(
        file_name,
        line_number,
        str(error)  # Converting the error object to string to include in the message
    )
    return error_message  # Return the complete formatted message


## Custom exception class to handle exceptions with detailed error messages
class CustomException(Exception):  # Inheriting from base Exception class
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Calling the constructor of the base Exception class
        # The base class stores the plain error message (optional in this case)

        # Store the formatted message with full context using the above function
        # So when the exception is raised, it includes file name, line number, and full message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message  # This method returns the string version of the error
        # Whenever the CustomException is printed or converted to string,
        # it will return the full detailed message instead of just the error text


# Example usage:
if __name__ == "__main__":
    try:
        # Simulating an error for demonstration
        1 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # Catching the exception and raising our custom exception with detailed message
        raise CustomException(e, sys) from e  # 'from e' keeps the original traceback context

