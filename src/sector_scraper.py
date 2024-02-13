"""
This module contains the SectorScraper class for scraping sector data from a specified URL.

The SectorScraper class is designed to fetch sector-specific information from a given webpage,
parse the fetched HTML content to extract relevant data using BeautifulSoup, and return the
data in a structured pandas DataFrame format. The class supports handling HTTP errors and
logging to facilitate debugging and monitoring of the scraping process.

The module sets up basic logging configuration upon import, ensuring that log messages are
appropriately formatted and logged to the console during execution.

Classes:
    SectorScraper: A class for scraping sector data from a website and returning it as a pandas DataFrame.

Functions:
    setup_logging(): Sets up basic logging configuration for the module.

Dependencies:
    - logging: Standard Python logging module for logging messages.
    - requests: Third-party library for making HTTP requests.
    - pandas: Third-party library providing high-performance, easy-to-use data structures.
    - BeautifulSoup (from bs4): Third-party library for parsing HTML and XML documents.

Example:
    scraper = SectorScraper("http://example.com/sectors")
    sector_data_df = scraper.fetch_sectors_data()
    print(sector_data_df)
"""

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
    :param url: The URL to scrape.
    :type url: str
    :return: None
    """

    def __init__(self, url):
        """
        Initialize the SectorScraper with the URL to scrape.
        :param url: The URL to scrape.
        :type url: str
        :return: None
        """
        self.url = url
        self.sectors_data = []

    def fetch_sectors_data(self):
        """
        Fetch sector data from the website and return it as a DataFrame.
        :return: The sector data.
        :rtype: pd.DataFrame
        :raises requests.RequestException: If an error occurs while fetching the data.
        :raises ValueError: If the response status code is not 200 (OK).
        :raises AttributeError: If an error occurs while parsing the response content.
        :raises TypeError: If an error occurs while parsing the response content.
        :raises IndexError: If an error occurs while parsing the response content.
        :raises Exception: If an error occurs while parsing the response content.
        """
        # Send a GET request to the URL
        response = requests.get(url=self.url)

        # If the response status code is not 200 (OK), log an error and return an empty DataFrame
        if response.status_code != 200:
            logging.error("Failed to retrieve data from %s }", self.url)
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
        logging.info("Sectors data successfully fetched from %s and parsed.", self.url)
        return pd.DataFrame(self.sectors_data)
