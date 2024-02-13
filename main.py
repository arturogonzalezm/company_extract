import logging
from src.data_processor import DataProcessor
from src.database_connection import DatabaseConnection
from src.log_config import setup_logging

# Set up logging configuration
setup_logging()


def main():
    """
    Main function of the application.

    This function gets a database connection, processes data from a CSV file and a web scraper, and stores the data in the database.
    If an error occurs during the data processing, it rolls back the database changes.
    Finally, it closes the database connection.
    """
    # Get a database connection
    conn = DatabaseConnection.get_connection()

    # If the database connection is None, log an error and return
    if conn is None:
        logging.error("Failed to get database connection.")
        return

    try:
        # Log a message indicating that the application is starting
        logging.info("Application is starting.")

        # Create a DataProcessor and process the data
        DataProcessor('data/companies.csv').process_data(conn)

        # Commit the database changes
        conn.commit()

        # Log a message indicating that the application finished successfully
        logging.info("Application finished successfully.")
    except Exception as e:
        # If an error occurs, log the error, roll back the database changes, and log a message indicating that
        # the changes were rolled back
        logging.error(f"An error occurred: {e}", exc_info=True)
        conn.rollback()
        logging.info("Database changes rolled back due to error.")
    finally:
        # Close the database connection and log a message indicating that the connection was closed
        conn.close()
        logging.info("Database connection closed.")


if __name__ == "__main__":
    # If the script is run directly (not imported), call the main function
    main()
