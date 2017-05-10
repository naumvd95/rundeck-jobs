import logging
from logging import config
import os

from devops_portal_tests.settings import CONSOLE_LOG_LEVEL
from devops_portal_tests.settings import LOGS_DIR


_log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s %(filename)s:'
                      '%(lineno)d -- %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': CONSOLE_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file_log': {
            'level': logging.DEBUG,
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.path.join(LOGS_DIR, 'tests.log'),
            'mode': 'w',
            'encoding': 'utf8',
        },
    },
    'loggers': {
        # Log all to log file , but by default only warnings.
        '': {
            'handlers': ['file_log'],
            'level': logging.DEBUG,
        },
        'tests': {
            'handlers': ['console'],
            'level': CONSOLE_LOG_LEVEL,
            'propagate': True
        },
    }
}

config.dictConfig(_log_config)
