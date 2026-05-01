import os
import logging
from datetime import datetime
import structlog


class CustomLogger():
    def __init__(self):
        # 1. create folder
        self.log_folder = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_folder, exist_ok=True)

        # 2. create filename path
        LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y')}.log"
        self.LOG_FILE_PATH = os.path.join(self.log_folder, LOG_FILE_NAME)

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter("%(message)s")

        # file handler
        file_handler = logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setFormatter(formatter)

        # console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


if __name__ == "__main__":
    loggerobj = CustomLogger()
    logger = loggerobj.get_logger()
    logger.info("I am calling from custom logger")
