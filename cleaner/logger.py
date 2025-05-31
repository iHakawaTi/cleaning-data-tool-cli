import logging


def setup_logger(log_path):
    """
    Create a logger that writes INFO-level logs to a file.
    Useful for tracking what operations the script performed.
    """
    logger = logging.getLogger('clean_logger')  # Unique logger name
    logger.setLevel(logging.INFO)  # Log all info and above (no debug)

    handler = logging.FileHandler(log_path)  # Log to file
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
