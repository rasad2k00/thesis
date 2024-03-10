import sys
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()


def setup_db_connection():
    conn = None
    try:
        conn = psycopg2.connect("")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logger.fatal(f"Database connection couldn't be created: {error}")
        sys.exit(1)


def write_to_database(conn, result):
    current_dt = datetime.now()
    id = int(round(current_dt.timestamp()))
    try:
        cur = conn.cursor()
        statement = f"""
        INSERT INTO results (id, result_data)
        VALUES
            (
                {id}, {result}
            );
        """
        cur.execute(statement)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Database error occured: {error}")
