import os
import logging
from datetime import datetime


class CustomLogger():
    def __init__(self):
        # 1create folder
        self.log_folder = os.path.join(os.getcwd(), "logs")

        # 2create filename path
        # LOG_FILE_NAME = f"{datetime.now().strftime("%d_%m_%Y")}.log"
        LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y')}.log"
        self.LOG_FILE_PATH = os.path.join(self.log_folder, LOG_FILE_NAME)
# for file handler

    def get_logger(self):
        file_handler = logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter("%(message)s")
        # "[%(asctime)s] %(levelname)s %(name)s (line:%lineno)d) - %(message)s")
# for console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter("%(message)s")
        # "[%(asctime)s] %(levelname)s %(name)s (line:%lineno)d) - %(message)s")

        # 3set logging configurations

        logging.basicConfig(
            filename=LOG_FILE_PATH,

            # level=logging.INFO,
            format="%(message)s",
            handlers=[file_handler, console_handler]
        )

        # filename=LOG_FILE_PATH,
        # format="[%(asctime)s] %(levelname)s %(name)s (line:%lineno)d) - %(message)s",
        # level=logging.INFO,
        return logging.getLogger(__name__)


if __name__ == "__main__":
    loggerobj = CustomLogger()
    logger = loggerobj.get_logger()
    logger.info("I am calling from custom logger")
