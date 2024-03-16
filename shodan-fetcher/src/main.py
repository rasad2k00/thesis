import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()

base_url = "https://api.shodan.io"

SEARCH_RESULTS_ENDPOINT = "/shodan/host/search"
CREDITS_COUNT_ENDPOINT = "/api-info"
RESULTS_COUNT_ENDPOINT = "/shodan/host/count"


def show_credits(keys, show_for_each_key=False):
    total_credits = 0
    total_available_credits = 0
    total_used_credits = 0
    credits = {}
    for key in keys:
        time.sleep(2)
        params = {"key": key}
        response = send_shodan_request(CREDITS_COUNT_ENDPOINT, **params).json()
        credits = 100
        available_credits = response["query_credits"]
        used_credits = credits - available_credits
        if show_for_each_key:
            print(f"[*] Key: {key}")
            print(f"[*]\tCredits: {credits}")
            print(f"[*]\tAvailable Credits: {available_credits}")
            print(f"[*]\tUsed Credits: {used_credits}")
        total_credits += credits
        total_available_credits += available_credits
        total_used_credits += used_credits
    print(f"[*] Total Credits: {total_credits}")
    print(f"[*] Total Available Credits: {total_available_credits}")
    print(f"[*] Total Used Credits: {total_used_credits}")


def search_shodan(keys, query):
    start_page = 1
    result_count = 1
    results = []
    params = {}
    for i in range(start_page, start_page + result_count):
        key = keys[i % len(keys)]
        params = {"key": key, "query": query, "page": i}
        response = send_shodan_request(SEARCH_RESULTS_ENDPOINT, **params)
        if response.status_code != 200:
            continue
        data = response.json()
        results.append(data)
        logger.info(f"Query run: {query}")
    write_to_json("shodan.json", results)


def send_shodan_request(endpoint, **kwargs):
    params = {}
    for k, v in kwargs.items():
        params[k] = v
    result = requests.get(base_url + endpoint, params=params)
    return result


def get_result_count(keys, query):
    params = {"key": keys[0], "query": query}
    response = send_shodan_request(RESULTS_COUNT_ENDPOINT, **params)
    count = response.json()["total"]
    return count


def write_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)


def read_keys():
    keys = os.getenv("SHODAN_KEYS")
    if keys is None:
        logger.fatal("No keys loaded!")
        sys.exit(1)
    return keys.split(":")


def main():
    keys = read_keys()
    # show_credits(keys=keys, show_for_each_key=True)
    query = "country:hu "
    if len(sys.argv) == 2:
        query += sys.argv[1]
    count = get_result_count(keys, query=query)
    print(f"[*] {query} - {count}")
    search_shodan(keys, query)


if __name__ == "__main__":
    main()
