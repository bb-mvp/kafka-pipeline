import os
import random
import time
from getgauge.python import step
import psycopg2
from psycopg2 import Error


def end_time(duration):
    return time.time() + int(duration)


def connection():
    return psycopg2.connect(
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USERNAME"),
        password=os.environ.get("DATABASE_PASSWORD"),
    )


def random_amount():
    return random.randint(1, 100000) / 100


@step("Add a transaction every <frequency> seconds for <duration> seconds")
def add_transactions(frequency, duration):
    print(
        f"Adding a transaction every {frequency} seconds for {duration} seconds . . ."
    )
    sql = """INSERT INTO transactions(amount, time)
             VALUES(%s, now()) RETURNING id;"""
    conn = None
    error = None
    try:
        conn = connection()
        cur = conn.cursor()
        t_end = end_time(duration)
        while time.time() < t_end:
            cur.execute(sql, (random_amount(),))
            time.sleep(int(frequency))
        conn.commit()
        cur.close()
    except (Exception, Error) as err:
        error = err
    finally:
        if conn is not None:
            conn.close()
        assert error is None, error
        print("Done")
