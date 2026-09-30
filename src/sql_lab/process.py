import logging
import os

import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_data(filename):
    logger.info("Reading data from %s", filename)
    data = pd.read_csv(filename)
    return data


def clean_data(data):
    logger.info("Cleaning data")
    cleaned_data = data.dropna()
    logger.info("Remaining rows after cleaning: %d", len(cleaned_data))
    return cleaned_data


def load_data(data, table):
    logger.info("Uploading data to table %s", table)
    host = os.environ["DBHOST"]
    database = os.environ["DBNAME"]
    user = os.environ["DBUSER"]
    password = os.environ["DBPASS"]

    try:
        connection_url = (
            f"mysql+mysqlconnector://{user}:{password}"
            f"@{host}:3306/{database}")
        engine = create_engine(connection_url)

        data.to_sql(
            table,
            con=engine,
            if_exists="replace",
            index=False)

        logger.info("Successfully uploaded %d rows", len(data))

    except Exception as error:
        logger.error("Error uploading data: %s", error)
        raise

    finally:
        if "engine" in locals():
            engine.dispose()


def main():
    filename = "MOCK_DATA.csv"
    data = read_data(filename)
    cleaned_data = clean_data(data)
    load_data(cleaned_data, "mock")


if __name__ == "__main__":
    main()
