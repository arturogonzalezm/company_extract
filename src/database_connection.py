import sqlite3


class DatabaseConnection:
    """
    Singleton class for managing a SQLite database connection.

    This class ensures that only one database connection is active at a time.
    The connection is established when get_connection() is called for the first time.
    """

    _instance = None
    _connection = None

    def __new__(cls):
        """
        Override the __new__ method to implement the Singleton pattern.

        This method ensures that only one instance of DatabaseConnection exists.
        If an instance already exists, it returns that instance.
        If not, it creates a new instance and initializes the _connection attribute to None.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._connection = None  # Ensure connection is initialized here or in get_connection
        return cls._instance

    @classmethod
    def get_connection(cls):
        """
        Get the active database connection.

        If a connection does not exist, it creates a new connection to the SQLite database.
        The database file is located at "db/companies.db".
        """
        if cls._connection is None:
            cls._connection = sqlite3.connect("db/companies.db")  # This should be caught by the mock
        return cls._connection
