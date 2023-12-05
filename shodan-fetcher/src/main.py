import os
import sys

from dotenv import load_dotenv
from logger import setup_logger
from shodan import Shodan

load_dotenv()
logger = setup_logger()


def search_shodan(clients, query):
    result = []
    result_count = 1
    for i in range(result_count):
        client = clients[i % len(clients)]
        result.append(client.search(query))
        logger.info(f"Query run: {query}")
    return result


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
    result = search_shodan(clients, query)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
