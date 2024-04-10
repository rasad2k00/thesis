import json
import sys
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()


def fetch_from_file(filename):
    results = {}
    with open(filename) as f:
        results = json.load(f)
    return results


def get_common_fields(results):
    common_fields = []
    for result in results:
        matches = result["matches"]
        for i in range(len(matches)):
            os = matches[i].get("os").replace("'", "") if matches[i].get("os") else None
            product = (
                matches[i].get("product").replace("'", "")
                if matches[i].get("product")
                else None
            )
            ip_str = matches[i].get("ip_str") if matches[i].get("ip_str") else None
            port = matches[i].get("port") if matches[i].get("port") else None
            org = (
                matches[i].get("org").replace("'", "")
                if matches[i].get("org")
                else None
            )
            timestamp = (
                matches[i].get("timestamp")
                if matches[i].get("timestamp")
                else datetime.now()
            )
            hostnames = (
                ",".join(matches[i].get("hostnames")).replace("'", "")
                if matches[i].get("hostnames")
                else None
            )
            domains = (
                ",".join(matches[i].get("domains")).replace("'", "")
                if matches[i].get("domains")
                else None
            )
            isp = (
                matches[i].get("isp").replace("'", "")
                if matches[i].get("isp")
                else None
            )
            hash = matches[i].get("hash") if matches[i].get("hash") else None
            version = matches[i].get("version") if matches[i].get("version") else None
            common_fields.append(
                [
                    os,
                    product,
                    ip_str,
                    port,
                    org,
                    timestamp,
                    hostnames,
                    domains,
                    isp,
                    hash,
                    version,
                ]
            )
    return common_fields


def setup_db_connection():
    conn = None
    try:
        conn = psycopg2.connect("")
        print("Connected to the database")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.fatal(f"Database connection couldn't be created: {error}")
        sys.exit(1)


def craete_table(conn):
    try:
        cur = conn.cursor()
        statement = """
        CREATE TABLE IF NOT EXISTS results
        (
            id SERIAL PRIMARY KEY,
            os VARCHAR(255),
            product TEXT,
            ip_str VARCHAR(255) NOT NULL,
            port INT NOT NULL,
            org TEXT,
            timestamp VARCHAR(255) NOT NULL,
            hostnames TEXT,
            domains TEXT,
            isp VARCHAR(255),
            hash INT,
            version VARCHAR(255)
        );
        """
        cur.execute(statement)
        conn.commit()
        print("Table created successfully")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Database error occured: {error}")


def write_to_database(conn, fields):
    cur = conn.cursor()
    try:
        for field in fields:
            statement = f"""
            INSERT INTO results (os, product, ip_str, port, org, timestamp, hostnames, domains, isp, hash, version)
            VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
            """
            cur.execute(statement, field)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Database error occured: {error}")


if __name__ == "__main__":
    conn = setup_db_connection()
    craete_table(conn)
    directory = "shodan-data/"
    filenames = [
        "shodan_camera.json",
        "shodan_data.json",
        "shodan_version.json",
        "shodan_http.json",
    ]
    for filename in filenames:
        results = fetch_from_file(directory + filename)
        common_fields = get_common_fields(results)
        write_to_database(conn, common_fields)
