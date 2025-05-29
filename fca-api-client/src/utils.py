def setup_logging_to_db(logger_name='default_logger', log_type='client'):
    """
    Set up logging to store logs in the database.

    Args:
        logger_name (str, optional): The name of the logger. Defaults to 'default_logger'.
        log_type (str, optional): Type of log ('client' or 'crud'). Defaults to 'client'.

    Returns:
        logging.Logger: A configured logger instance.
    """
    import logging
    from sqlalchemy.orm import sessionmaker
    from config import engine
    from db_models import ClientLogTable, CrudLogTable
    from datetime import datetime, timezone

    # Create a logger with the specified name
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        class DBHandler(logging.Handler):
            def emit(self, record):
                session = sessionmaker(bind=engine)()
                try:
                    log_entry = None
                    if log_type == 'client':
                        log_entry = ClientLogTable(
                            timestamp= datetime.fromtimestamp(record.created, tz=timezone.utc),
                            log_level=record.levelname,
                            log_message=record.message
                        )
                    elif log_type == 'crud':
                        log_entry = CrudLogTable(
                            timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc),
                            log_level=record.levelname,
                            log_message=record.message
                        )
                    if log_entry:
                        session.add(log_entry)
                        session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"Failed to log to database: {e}")
                finally:
                    session.close()

        # Add the database handler to the logger
        db_handler = DBHandler()
        logger.addHandler(db_handler)

    return logger