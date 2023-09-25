import logging
import sys

# Setting up logger with the appropriate handler
def setup_logger(log_level=logging.DEBUG, filename="shodan-fetcher.log"):
    logging.basicConfig(filename=filename)
    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    logger.addHandler(handler)
    return logger
    