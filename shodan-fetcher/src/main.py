from shodan import Shodan
from logger import setup_logger
import sys
import os

logger = setup_logger()


def search_shodan(api, query):
    # Make a shodan query
    result = api.search('country:hu')
    logger.info(f"Query run")

def setup_shodan_connection():
    api_key = os.getenv("SHODAN_API_KEY")
    if api_key is None:
        logger.info("Please provide your API key!")
        sys.exit(-1)
    api = Shodan(api_key)
    return api


def main():
    api = setup_shodan_connection()
    search_shodan(api)


if __name__ == "__main__":
    main()
