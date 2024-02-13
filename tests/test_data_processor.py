import pytest
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock
from src.data_processor import DataProcessor
from src.sector_scraper import SectorScraper


# Create a fixture for the DataProcessor instance
@pytest.fixture
def data_processor():
    return DataProcessor('data/companies.csv')


# Test the __init__ method
def test_init(data_processor):
    assert data_processor.file_path == 'data/companies.csv'


# Test the process_data method
@patch.object(SectorScraper, 'fetch_sectors_data')
@patch('pandas.read_csv')
def test_process_data(mock_read_csv, mock_fetch_sectors_data, data_processor):
    # Mock the response from SectorScraper.fetch_sectors_data and pd.read_csv
    mock_fetch_sectors_data.return_value = pd.DataFrame([{'SECTOR': 'Test Sector', 'REPORT_COUNT': 5}])
    mock_read_csv.return_value = pd.DataFrame([{'COMPANY': 'Test Company', 'SECTOR': 'Test Sector'}])

    # Create a mock sqlite3 connection
    conn = sqlite3.connect(":memory:")

    # Call the method and check the result
    data_processor.process_data(conn)

    # Check that the tables were created in the database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    assert ('LDS_SECTOR',) in tables
    assert ('LDS_COMPANIES',) in tables
    assert ('PDS_COMPANIES',) in tables
    assert ('RDS_COMPANIES',) in tables
