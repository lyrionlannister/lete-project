import os
import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
        )

        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        file_handler = logging.FileHandler("./logs/app.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            # env = os.getenv("ENVIRONMENT", "development")
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns the logger instance.
        """
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance.logger
    
    
