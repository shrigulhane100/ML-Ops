import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    """
    Takes an error message and its details and returns a formatted error message string.

    Parameters:
        error (Any): The error message.
        error_detail (sys): The error details.

    Returns:
        str: The formatted error message string.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    # This code defines a special method called __str__ in a class. When an instance of the class is converted 
    # to a string, this method will be called and it will return the value of the error_message attribute of 
    # that instance.
    def __str__(self):
        """
        Return a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """
        return self.error_message
    

# if __name__ == "__main__":
#     try:
#         a= 1/0
#     except Exception as e:
#         logging.info('Divide by zero')
#         raise CustomException(e, sys)
