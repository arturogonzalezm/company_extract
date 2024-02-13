import pytest
import requests
from src.sector_scraper import SectorScraper
from unittest.mock import patch


# Create a fixture for the SectorScraper instance
@pytest.fixture
def scraper():
    return SectorScraper('https://www.ibisworld.com/au/list-of-enterprise-profiles/#administrative-and-support-services')


# Test the __init__ method
def test_init(scraper):
    assert scraper.url == 'https://www.ibisworld.com/au/list-of-enterprise-profiles/#administrative-and-support-services'
    assert scraper.sectors_data == []


# Test the fetch_sectors_data method
@patch('requests.get')
def test_fetch_sectors_data(mock_get, scraper):
    # Mock the response from requests.get
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = """
    <div class="col-sm-4">
        <div class="SectorTitle">Test Sector</div>
        <div class="ReportCount">5 Reports</div>
    </div>
    """

    # Call the method and check the result
    scraper.fetch_sectors_data()
    assert scraper.sectors_data == [{'SECTOR': 'Test Sector', 'REPORT_COUNT': 5}]
