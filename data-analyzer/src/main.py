import json
import sys


def fetch_from_file(filename):
    with open(filename) as f:
        results = json.load(f)
        for result in results:
            matches = result["matches"]
            for i in range(len(matches)):
                os = matches[i].get("os")
                product = matches[i].get("product")
                ip_str = matches[i].get("ip_str")
                port = matches[i].get("port")
                org = matches[i].get("org")
                timestamp = matches[i].get("timestamp")
                hostnames = matches[i].get("hostnames")
                domains = matches[i].get("domains")
                isp = matches[i].get("isp")
                hash = matches[i].get("hash")
                print(f"#{i}:")
                print(f"\tOS: {os}")
                print(f"\tProduct: {product}")
                print(f"\tIP: {ip_str}")
                print(f"\tPort: {port}")
                print(f"\tOrg: {org}")
                print(f"\tTimestamp: {timestamp}")
                print(f"\tHostnames: {hostnames}")
                print(f"\tDomains: {domains}")
                print(f"\tISP: {isp}")
                print(f"\tHash: {hash}")
            sys.exit()


def main():
    filename = "shodan_data.json"
    fetch_from_file(filename)


if __name__ == "__main__":
    main()
