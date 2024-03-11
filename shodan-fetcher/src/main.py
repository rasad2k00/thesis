import json
import os
import sys

import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()


def search_shodan(keys, query):
    start_page = 1
    result_count = 100
    results = []
    for i in range(start_page, start_page + result_count):
        key = keys[i % len(keys)]
        response = send_shodan_request(key, query, page=i)
        if response.status_code != 200:
            continue
        data = response.json()
        results.append(data)
        logger.info(f"Query run: {query}")
    with open("shodan_data.json", "w") as f:
        json.dump(results, f)


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
