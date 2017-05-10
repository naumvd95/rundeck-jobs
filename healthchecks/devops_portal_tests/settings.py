import logging
import os


# Logging settings
CONSOLE_LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.DEBUG)
LOGS_DIR = os.environ.get('LOG_DIR', os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir)))

# env configuration

CONFIG_FILE_PATH = os.environ.get('CONFIG_FILE_PATH', None)
