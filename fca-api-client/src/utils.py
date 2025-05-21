def rate_limiter(max_requests_per_minute):
    """
    Limit the rate of function calls to a specified number per minute.

    This function acts as a decorator to enforce rate limiting on the decorated function.
    It depends on:
    - The `time` module for tracking elapsed time and sleeping.
    - The `functools.wraps` decorator to preserve the original function's metadata.

    Args:
        max_requests_per_minute (int): The maximum number of allowed requests per minute.

    Returns:
        Callable: A decorated function with rate limiting applied.
    """
    import time
    from functools import wraps

    interval = 60 / max_requests_per_minute
    last_call = [0.0]  # Start with 0.0

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if last_call[0] != 0.0:
                elapsed = now - last_call[0]
                if elapsed < interval:
                    time.sleep(interval - elapsed)
            last_call[0] = now
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_with_exponential_backoff(max_retries, base_delay=1, max_delay=60):
    """
    Retry a function with exponential backoff in case of exceptions.

    This function acts as a decorator to retry the decorated function up to a specified
    number of times, with an exponentially increasing delay between retries. It depends on:
    - The `time` module for sleeping between retries.
    - The `functools.wraps` decorator to preserve the original function's metadata.

    Args:
        max_retries (int): The maximum number of retry attempts.
        base_delay (int, optional): The initial delay in seconds. Defaults to 1.
        max_delay (int, optional): The maximum delay in seconds. Defaults to 60.

    Returns:
        Callable: A decorated function with retry logic applied.
    """
    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait_time = min(base_delay * (2 ** retries), max_delay)
                    time.sleep(wait_time)
                    retries += 1
            raise Exception(f"Function {func.__name__} failed after {max_retries} retries.")

        return wrapper

    return decorator


def setup_logging(log_file='api_client.log'):
    """
    Set up logging for the application.

    This function configures the logging module to log messages to a specified file
    with a consistent format. It depends on:
    - The `logging` module for logging configuration and message handling.

    Args:
        log_file (str, optional): The name of the log file. Defaults to 'api_client.log'.

    Returns:
        logging.Logger: A configured logger instance.
    """
    import logging

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    return logging.getLogger()