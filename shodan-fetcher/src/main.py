import os
import sys

from dotenv import load_dotenv
from psycopg2.extras import Json
from shodan import Shodan

from utils.db import setup_db_connection, write_to_database
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger()


def sanitize_json(data):
    data = Json(str(data).replace("\u0000", ""))
    return data


def search_shodan(clients, query, conn):
    result_count = 50
    for i in range(1, result_count + 1):
        client = clients[i % len(clients)]
        # In order to get multiple pages of results,
        # we can use page parameter in search function
        result = client.search(query, page=i)
        data = sanitize_json(result)
        write_to_database(conn, data)
        logger.info(f"Query run: {query}")


def get_shodan_clients(keys):
    clients = []
    for key in keys:
        client = Shodan(key)
        clients.append(client)
    return clients


def read_keys():
    keys = os.getenv("SHODAN_KEYS")
    if keys is None:
        logger.fatal("No keys loaded!")
        sys.exit(1)
    return keys.split(":")


def main():
    keys = read_keys()
    clients = get_shodan_clients(keys)
    query = "country:hu"
    conn = setup_db_connection()
    search_shodan(clients, query, conn)


if __name__ == "__main__":
    main()
