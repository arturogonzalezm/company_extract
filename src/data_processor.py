import logging
import pandas as pd
from src.log_config import setup_logging
from src.sector_scraper import SectorScraper

# Set up logging configuration
setup_logging()


class DataProcessor:
    """
    Class for processing data from a CSV file and a web scraper.

    This class reads data from a CSV file and a web scraper, processes the data, and stores it in a database.
    """

    def __init__(self, file_path):
        """
        Initialize the DataProcessor with the path to the CSV file.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path

    def process_data(self, conn):
        """
        Process the data from the CSV file and the web scraper and store it in the database.

        This method fetches data from a web scraper, processes it, and stores it in the database.
        It then reads data from a CSV file, processes it, and stores it in the database.
        Finally, it merges the data from the CSV file and the web scraper, processes it, and stores it in the database.

        Args:
            conn (sqlite3.Connection): The database connection.

        Returns:
            None
        """
        # Create a SectorScraper and fetch the sectors data
        sector_scraper = SectorScraper(
            "https://www.ibisworld.com/au/list-of-enterprise-profiles/#administrative-and-support-services")
        df_sectors = sector_scraper.fetch_sectors_data()

        # If no sectors data was fetched, log a warning and return
        if df_sectors.empty:
            logging.warning("No sector data fetched. Check scraper or source website.")
            return

        # Process the sectors data and store it in the database
        df_sectors = df_sectors.reset_index().rename(columns={'index': 'SECTOR_ID'})
        df_sectors.to_sql("LDS_SECTOR", conn, if_exists="replace", index=False)
        logging.info("Sector data processed and stored in database.")

        # Try to read the companies data from the CSV file, process it, and store it in the database
        try:
            pd.read_csv(self.file_path).to_sql('LDS_COMPANIES', conn, if_exists='replace', index=False)
            logging.info("Companies data loaded and stored in database.")
        except Exception as e:
            logging.error(f"Failed to process companies data from {self.file_path}: {e}")

        # Read the companies and sectors data from the database
        company_df = pd.read_sql_query('SELECT * FROM LDS_COMPANIES', conn)
        sector_df = pd.read_sql_query('SELECT * FROM LDS_SECTOR', conn)

        # Merge the companies and sectors data, process it, and store it in the database
        merged_df = pd.merge(company_df, sector_df[['SECTOR_ID', 'SECTOR']], on='SECTOR', how='left')
        merged_df.drop(columns=['SECTOR'], inplace=True)
        merged_df.to_sql('PDS_COMPANIES', conn, if_exists='replace', index=False)
        logging.info("Company and sector data merged and updated.")

        # Create the final joined data and store it in the database
        query = """
                SELECT LDS_SECTOR.SECTOR_ID,
                LDS_SECTOR.SECTOR,
                PDS_COMPANIES.COMPANY,
                LDS_SECTOR.REPORT_COUNT
                   FROM PDS_COMPANIES
                   LEFT JOIN LDS_SECTOR ON PDS_COMPANIES.SECTOR_ID = LDS_SECTOR.SECTOR_ID;
                """
        pd.read_sql_query(query, conn).to_sql('RDS_COMPANIES', conn, if_exists='replace', index=False)
        logging.info("Final joined data created and stored in database.")