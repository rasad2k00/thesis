import json


def fetch_from_file(filename):
    with open(filename) as f:
        buf = f.read()
        data = json.loads(buf)
        for match in data["matches"][:1]:
            for k, v in match.items():
                print(f"{k}: {v}")


def main():
    filename = "shodan_data.txt"
    fetch_from_file(filename)


if __name__ == "__main__":
    main()
