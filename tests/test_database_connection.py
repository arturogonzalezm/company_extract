import pytest
from unittest.mock import patch, MagicMock

from src.database_connection import DatabaseConnection


# Adjust the import path according to your project structure


@pytest.fixture
def reset_database_connection_singleton():
    DatabaseConnection._instance = None
    DatabaseConnection._connection = None
    yield
    DatabaseConnection._instance = None
    DatabaseConnection._connection = None


def test_singleton_implementation(reset_database_connection_singleton):
    db_conn1 = DatabaseConnection()
    db_conn2 = DatabaseConnection()
    assert db_conn1 is db_conn2, "DatabaseConnection does not implement Singleton pattern correctly"


@patch('sqlite3.connect', return_value=MagicMock())
def test_lazy_initialization_of_connection(mock_connect, reset_database_connection_singleton):
    # Before calling get_connection, _connection should be None
    assert DatabaseConnection._connection is None, "Connection should be None before any call to get_connection"
    connection = DatabaseConnection.get_connection()
    assert connection is not None, "get_connection should return a connection"
    mock_connect.assert_called_once_with("db/companies.db"), "sqlite3.connect was not called correctly"


@patch('sqlite3.connect', return_value=MagicMock())
def test_get_connection_returns_same_connection_object(mock_connect, reset_database_connection_singleton):
    connection1 = DatabaseConnection.get_connection()
    connection2 = DatabaseConnection.get_connection()
    assert connection1 is connection2, "get_connection should return the same connection object on subsequent calls"
    mock_connect.assert_called_once(), "sqlite3.connect should be called exactly once"
