"""
This module provides a singleton DatabaseConnection class for managing
database connections. It ensures that only one connection is active at a time
and provides a consistent interface for fetching the current database connection.
"""


import sqlite3
import logging

from src.log_config import setup_logging

setup_logging()


class DatabaseConnection:
    """
    Singleton class for managing database connections.
    :cvar _instance: The instance of the class.
    :cvar _connection: The database connection.
    """

    _instance = None
    _connection = None

    def __new__(cls):
        """
        Create a new instance of the class if it does not exist.
        :return: The instance of the class.
        :rtype: DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._connection = None  # Ensure connection is initialized here or in get_connection
            logging.info("DatabaseConnection instance created.")
        return cls._instance

    @classmethod
    def get_connection(cls):
        """
        Get the current database connection. If no connection exists, create a new one.
        :return: The database connection.
        :rtype: sqlite3.Connection
        """
        if cls._connection is None:
            try:
                cls._connection = sqlite3.connect("db/companies.db")
                logging.info("New database connection created.")
            except sqlite3.Error as error:
                cls._connection = None  # Ensure that _connection is reset in case of failure
                logging.error(f"Failed to create database connection: {error}")
                raise  # Optionally, re-raise the exception to be handled by the caller
        return cls._connection
