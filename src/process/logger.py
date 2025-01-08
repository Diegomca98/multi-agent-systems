import os
import logging
from datetime import datetime
import sys
import traceback

class Logger:
    _instance = None
    _log_file = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._initialize_logging()
        return cls._instance

    @classmethod
    def _initialize_logging(cls):
        # Logs dir
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cls._log_file = os.path.join(log_dir, f'app_log_{timestamp}.log')

        # Create file handler with explicit permission settings
        try:
            file_handler = logging.FileHandler(cls._log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)8s | %(module)20s | %(funcName)20s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)

            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.DEBUG)
            
            # Remove any existing handlers to prevent duplicate logging
            root_logger.handlers.clear()
            
            # Add file handler
            root_logger.addHandler(file_handler)

            # Optionally add console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(file_formatter)
            root_logger.addHandler(console_handler)

            # Ensure logs are written immediately
            logging.getLogger().handlers[0].flush()

            print(f"Log file initialized at: {cls._log_file}")
        except Exception as e:
            print(f"Error initializing logger: {e}")
            traceback.print_exc()

    def get_logger(self, name = None):
        return logging.getLogger(name)

    def log_debug(self, message, module_name=None):
        logger = self.get_logger(module_name)
        logger.debug(message)

    def log_info(self, message, module_name=None):
        logger = self.get_logger(module_name)
        logger.info(message)

    def log_warning(self, message, module_name=None):
        """Log a warning message"""
        logger = self.get_logger(module_name)
        logger.warning(message)

    def log_error(self, message, module_name=None, exec_info=False):
        """
        Log an error message
        
        :param message: Error message
        :param module_name: Name of the module
        :param exc_info: Whether to include exception traceback
        """
        logger = self.get_logger(module_name)
        if exec_info:
            logger.error(message, exc_info=True)
        else:
            logger.error(message)

    def log_critical(self, message, module_name=None):
        logger = self.get_logger(module_name)
        logger.critical(message)

    @classmethod
    def get_log_file_path(cls):
        return cls._log_file