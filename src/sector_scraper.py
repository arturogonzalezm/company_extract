import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

from src.log_config import setup_logging

# Set up logging configuration
setup_logging()


class SectorScraper:
    """
    Class for scraping sector data from a website.

    This class uses the BeautifulSoup library to scrape sector data from a given URL.
    The scraped data is stored in a pandas DataFrame and can be retrieved using the fetch_sectors_data method.
    """

    def __init__(self, url):
        """
        Initialize the SectorScraper with the URL to scrape.

        Args:
            url (str): The URL to scrape.
        """
        self.url = url
        self.sectors_data = []

    def fetch_sectors_data(self):
        """
        Fetch the sectors data from the URL.

        This method sends a GET request to the URL and parses the response content with BeautifulSoup.
        It then extracts the sector data from the parsed content and stores it in a pandas DataFrame.

        Returns:
            A pandas DataFrame containing the sectors data, or an empty DataFrame if an error occurred.
        """
        # Send a GET request to the URL
        response = requests.get(url=self.url)

        # If the response status code is not 200 (OK), log an error and return an empty DataFrame
        if response.status_code != 200:
            logging.error(f"Failed to retrieve data from {self.url}")
            return pd.DataFrame()

        # Parse the response content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all div elements with class 'col-sm-4'
        sector_divs = soup.find_all('div', class_='col-sm-4')

        # For each div element, extract the sector title and report count and append them to the sectors data
        for business_div in sector_divs:
            sector_title_div = business_div.find('div', class_='SectorTitle')
            report_count_div = business_div.find('div', class_='ReportCount')

            if sector_title_div and report_count_div:
                sector_title = sector_title_div.text.strip()
                report_count = int(report_count_div.text.split()[0])
                self.sectors_data.append({"SECTOR": sector_title, "REPORT_COUNT": report_count})

        # Log a success message and return a DataFrame containing the sectors data
        logging.info(f"Sectors data successfully fetched from {self.url}")
        return pd.DataFrame(self.sectors_data)