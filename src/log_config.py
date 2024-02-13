import logging


def setup_logging():
    """
    Sets up the basic configuration for logging.

    This function sets the logging level to INFO, which means that INFO, WARNING, ERROR, and CRITICAL messages will be logged.
    DEBUG messages will not be logged because they have a lower priority than INFO.

    The format for the log messages is set to include the time of logging, the severity level of the message, the name of the logger, and the log message itself.

    The time is formatted as 'Year-Month-Day Hour:Minute:Second'.

    This function does not take any parameters and does not return anything.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
