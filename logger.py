# logger.py

import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO)

def get_logger(name):
    return logging.getLogger(name)
