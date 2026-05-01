

from src.logger import GLOBAL_LOGGER as log
from src.exception.custom_exception import CustomException
import logging
import sys
from pathlib import Path


def add(a, b):
    log.info("started add method")
    try:
        a = 9/0
    except Exception as e:
        log.error(e)
        # log.error(str(CustomException(e, sys)))
        # three scenarios we are handling
        # customobj=CustomException("Division failed")
        # customobj=CustomException("Division failed", sys)
        # customobj=CustomException("Division failed", e)
        # print(customobj) # it will call __str__ method
        raise CustomException("Division failed", sys)


if __name__ == "__main__":
    try:
        add(2, 3)
    except CustomException as e:
        log.error(str(e))


# from src.logger.custom_logger import CustomLogger
# # import logging
# # import os

# loggerobj = CustomLogger()
# logger = loggerobj.get_logger(__file__)


# def add(a, b):
#     logger.info("started add method", a=a, b=b)
#     sum = a+b
#     sum(a, b)
#     logger.info("ended add method", sum=sum)
#     return sum, a, b


# def sum(a, b):
#     logger.info("started add method")
#     try:
#         pass
#     except Exception as e:

#         sum = a+b
#         logger.info("ended add method")
#     return sum


# if __name__ == "__main__":
#     a, _, _ = add(2, 3)
