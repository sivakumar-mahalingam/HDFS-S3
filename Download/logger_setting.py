import sys
import logging
from logging.config import dictConfig
from datetime import datetime
import configparser

config_path = '/edgenode/s3/download/s3_config.conf'
configuration_file = configparser.ConfigParser()
config = configuration_file.read_file(open(config_path))

log_file_path = configuration_file.get('config', 'log_file_path')

logging_config = dict(
    version=1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'py-logger': {'class': 'logging.handlers.TimedRotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': datetime.now().strftime(log_file_path+'_%d_%m_%Y.log')},
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    loggers={
        'py_logger': {
            'handlers': ['py-logger', 'console'],
            'level': logging.DEBUG
        }
    }
)

dictConfig(logging_config)

