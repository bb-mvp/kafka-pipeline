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
        port=os.environ.get("DATABASE_PORT"),
    )


def random_amount():
    return random.randint(1, 100000) / 100


def random_tran_id():
    return random.randint(1, 100000000)


def random_currency():
    list_currency = ["RON", "EUR", "USD"]
    return random.choice(list_currency)


def random_debit_credit():
    list_d_c = ["D", "C"]
    return random.choice(list_d_c)


def random_tran_status():
    list_statuses = ["Pending", "Processed"]
    return random.choice(list_statuses)


def random_iban():
    list_ibans = [
        "RO30BRDE450SV22222200002",
        "RO73BRDE450SV22222200004",
        "RO44BRDE450CR22222200010",
    ]
    return random.choice(list_ibans)


@step("Add a transaction every <frequency> seconds for <duration> seconds")
def add_transactions(frequency, duration):
    print(
        f"Adding a transaction every {frequency} seconds for {duration} seconds . . ."
    )

    sql = """INSERT INTO transaction(
             transaction_id, type, type_group, description, booking_date, credit_debit, transaction_currency,amount, status, customer_id, source_account, destination_account)
             VALUES (%s, 'ATM', 'ATM', 'Description for ', CURRENT_DATE, %s, %s, %s,%s, '22222200', 'RO57BRDE450SV22222200001', %s);"""
    conn = None
    error = None
    try:
        conn = connection()
        cur = conn.cursor()
        t_end = end_time(duration)
        while time.time() < t_end:
            cur.execute(
                sql,
                (
                    random_tran_id(),
                    random_debit_credit(),
                    random_currency(),
                    random_amount(),
                    random_tran_status(),
                    random_iban(),
                ),
            )
            conn.commit()
            time.sleep(int(frequency))

        cur.close()
    except (Exception, Error) as err:
        error = err
    finally:
        if conn is not None:
            conn.close()
        assert error is None, error
        print("Done")
