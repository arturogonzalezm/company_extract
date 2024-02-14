# Module docstring: This module contains the DataProcessor class for processing data from CSV files and web scrapers.

import logging
import pandas as pd
from src.log_config import setup_logging
from src.sector_scraper import SectorScraper

# Set up logging configuration
setup_logging()


class DataProcessor:
    """
    Class for processing data from a CSV file and a web scraper.
    :param file_path: The path to the CSV file.
    :type file_path: str
    """

    def __init__(self, file_path):
        """
        Initialize the DataProcessor with the path to the CSV file.
        """
        self.file_path = file_path

    def process_data(self, conn):
        """
        Process the data from the CSV file and the web scraper and store it in the database.
        :param conn: The database connection.
        :type conn: sqlite3.Connection
        """
        sector_scraper = SectorScraper(
            "https://www.ibisworld.com/au/list-of-enterprise-profiles/"
            "#administrative-and-support-services")
        df_sectors = sector_scraper.fetch_sectors_data()

        if df_sectors.empty:
            logging.warning("No sector data fetched. Check scraper or source website.")
            return

        df_sectors = df_sectors.reset_index().rename(columns={'index': 'SECTOR_ID'})
        df_sectors.to_sql("LDS_SECTOR", conn, if_exists="replace", index=False)
        logging.info("Sector data processed and stored in database.")

        try:
            pd.read_csv(self.file_path).to_sql('LDS_COMPANIES', conn, if_exists='replace', index=False)
            logging.info("Companies data loaded and stored in database.")
        except pd.errors.ParserError as e:
            logging.error("Failed to process companies data from %s %s:", self.file_path, e)

        company_df = pd.read_sql_query('SELECT * FROM LDS_COMPANIES', conn)
        sector_df = pd.read_sql_query('SELECT * FROM LDS_SECTOR', conn)

        merged_df = pd.merge(company_df, sector_df[['SECTOR_ID', 'SECTOR']], on='SECTOR', how='left')
        merged_df.drop(columns=['SECTOR'], inplace=True)
        merged_df.to_sql('PDS_COMPANIES', conn, if_exists='replace', index=False)
        logging.info("Company and sector data merged and updated.")

        query = """
                SELECT LDS_SECTOR.SECTOR_ID, LDS_SECTOR.SECTOR, PDS_COMPANIES.COMPANY, LDS_SECTOR.REPORT_COUNT
                FROM PDS_COMPANIES
                LEFT JOIN LDS_SECTOR ON PDS_COMPANIES.SECTOR_ID = LDS_SECTOR.SECTOR_ID;
                """
        pd.read_sql_query(query, conn).to_sql('RDS_COMPANIES', conn, if_exists='replace', index=False)
        logging.info("Final joined data created and stored in database.")
