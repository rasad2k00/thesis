import os
import sys

import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()


def write_to_file(data, filename="shodan_data.txt"):
    with open(filename, "a") as f:
        f.write(data)
        f.close()


def search_shodan(keys, query):
    result_count = 400
    for i in range(1, result_count + 1):
        key = keys[i % len(keys)]
        result = send_shodan_request(key, query, page=i)
        if result.status_code != 200:
            continue
        write_to_file(result.text)
        logger.info(f"Query run: {query}")


def send_shodan_request(key, query, page=1):
    base_url = "https://api.shodan.io/shodan/host/search"
    params = {"query": query, "page": page, "key": key}
    result = requests.get(base_url, params=params)
    return result


def read_keys():
    keys = os.getenv("SHODAN_KEYS")
    if keys is None:
        logger.fatal("No keys loaded!")
        sys.exit(1)
    return keys.split(":")


def main():
    keys = read_keys()
    query = "country:hu"
    search_shodan(keys, query)


if __name__ == "__main__":
    main()
