import logging
import os

import mysql.connector


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    host = os.environ["DBHOST"]
    database = os.environ["DBNAME"]
    user = os.environ["DBUSER"]
    password = os.environ["DBPASS"]

    return mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,)

def get_data_by_group(value):
    logger.info("Getting rows where group = %s", value)

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT *
            FROM mock
            WHERE `group` = %s
        """

        cursor.execute(query, (value,))

        results = cursor.fetchall()

        logger.info("Retrieved %d rows", len(results))
        return results

    except Exception as error:
        logger.error("Error querying data: %s", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def plot_counts(groupby):
    logger.info("Counting rows grouped by %s", groupby)

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        allowed_columns = [
            "id",
            "group",
            "first_name",
            "last_name",
            "email",
            "join_date",]

        if groupby not in allowed_columns:
            raise ValueError(f"Invalid column name: {groupby}")

        query = f"""
            SELECT `{groupby}`, COUNT(*)
            FROM mock
            GROUP BY `{groupby}`
            ORDER BY COUNT(*) DESC
        """

        cursor.execute(query)

        results = cursor.fetchall()

        logger.info("Retrieved counts for %d groups", len(results))
        return results

    except Exception as error:
        logger.error("Error counting data: %s", error)
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def main():
    results = get_data_by_group("Item 1")

    print("Rows in Item 1:")
    for row in results:
        print(row)

    counts = plot_counts("group")


if __name__ == "__main__":
    main()
