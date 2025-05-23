def setup_logging(log_file='fca_api.log', logger_name='default_logger'):
    """
    Set up logging for the application.

    This function configures the logging module to log messages to a specified file
    with a consistent format. It depends on:
    - The `logging` module for logging configuration and message handling.

    Args:
        log_file (str, optional): The name of the log file. Defaults to 'fca_api.log'.
        logger_name (str, optional): The name of the logger. Defaults to 'default_logger'.

    Returns:
        logging.Logger: A configured logger instance.
    """
    import logging

    # Create a logger with the specified name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Create a file handler for the log file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

    return logger