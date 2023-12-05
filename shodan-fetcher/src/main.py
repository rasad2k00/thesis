import os
import sys

from logger import setup_logger
from shodan import Shodan

logger = setup_logger()


def search_shodan(client, query):
    # Make a shodan query
    result = client.search(query)
    logger.info(f"Query run: {query}")
    return result


def get_shodan_client():
    key = os.getenv("SHODAN_KEY")
    if key is None:
        logger.info("Please provide your API key!")
        sys.exit(1)
    client = Shodan(key)
    return client


def main():
    client = get_shodan_client()
    query = "country:hu"
    result = search_shodan(client, query)
    print(f"[*] Result: {result}")


if __name__ == "__main__":
    main()
