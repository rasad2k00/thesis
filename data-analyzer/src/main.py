import json
import sys


def fetch_from_file(filename):
    results = {}
    with open(filename) as f:
        results = json.load(f)
    return results


def get_common_fields(results):
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
            version = matches[i].get("version")
            vulns = matches[i].get("vulns")
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
            print(f"\tVersion: {version}")
            for vuln, v in vulns.items():
                print(f"\tVuln: {vuln}, CVSS: {v.get('cvss')}")
            break
        break


def get_available_keys(results):
    available_keys = set()
    for result in results:
        matches = result["matches"]
        for match in matches:
            for k, _ in match.items():
                if k not in available_keys:
                    available_keys.add(k)
    return available_keys


def get_product_version(results):
    for result in results:
        matches = result["matches"]
        i = 0
        for match in matches:
            product = match.get("product", "Not found")
            version = match.get("version", 0)
            print(f"#{i:2}: {product} - {version}")
            i += 1


def main():
    if len(sys.argv) != 2:
        print("[*] Please provide a filename")
        sys.exit(1)
    filename = sys.argv[1]
    results = fetch_from_file(filename=filename)
    get_common_fields(results)


if __name__ == "__main__":
    main()
