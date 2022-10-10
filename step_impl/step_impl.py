import os
import random
import time
from getgauge.python import step
import psycopg2


def end_time(duration):
    return time.time() + int(duration)


def connection():
    return psycopg2.connect(
        host=os.environ.get('PGHOST'),
        database=os.environ.get('DATABASE_NAME'),
        user=os.environ.get('LIQUIBASE_COMMAND_USERNAME'),
        password=os.environ.get('LIQUIBASE_COMMAND_PASSWORD'))

def random_amount():
    return random.randint(1, 100000)/100


@step("Add a transaction every <frequency> seconds for <duration> seconds")
def add_transactions(frequency, duration):
    print("Adding transactions . . ")
    sql = """INSERT INTO transactions(amount, time)
             VALUES(%s, now()) RETURNING id;"""
    conn = None
    try:
        conn = connection()
        cur = conn.cursor()
        t_end = end_time(duration)
        while time.time() < t_end:
            cur.execute(sql, (random_amount(),))
            time.sleep(int(frequency))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
