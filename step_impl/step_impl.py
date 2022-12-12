import os
import random
import time
import datetime
import csv
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


def random_channel():
    channels = ["MOC", "IOC"]
    return random.choice(channels)


def random_pay_type():
    types = ["EFI", "EXS", "ISO", "XCH"]
    return random.choice(types)


def mc_payment_csv(transaction_id):

    today = datetime.datetime.now
    csv_file_name = "./sample_data/payment.csv"

    # list of fields name for mc_payment
    fields_name = [
        "BRCH",
        "APPLICATION",
        "CORRELATION_ID",
        "BFO_TRANSACTION_ID",
        "TRANSACTION_TYPE",
        "SOURCE_ACCOUNT",
        "SOURCE_ACCOUNT_OWNERID",
        "SOURCE_ACCOUNT_OWNERNAME",
        "SOURCE_ACCOUNT_TYPE",
        "SOURCE_ACCOUNT_CURRENCY",
        "TARGET_ACCOUNT",
        "TARGET_ACCOUNT_OWNERID",
        "TARGET_ACCOUNT_OWNERNAME",
        "TARGET_ACCOUNT_TYPE",
        "TARGET_ACCOUNT_CURRENCY",
        "TRANSACTION_CURRENCY",
        "TRANSACTION_AMOUNT",
        "TRANSACTION_VALUEDATE",
        "TRANSACTION_DESCRIPTION",
    ]

    rows = [
        [
            "4500",
            random_channel(),
            transaction_id,
            transaction_id,
            random_pay_type(),
            "RO57BRDE450SV22222200001",
            "22222200",
            "Peter",
            "SV",
            "RON",
            random_iban(),
            "22222200",
            "Peter",
            "SV",
            random_currency(),
            random_currency(),
            random_amount(),
            today(),
            "TRANSACTION_DESCRIPTION",
        ]
    ]

    # writing to csv file
    with open(csv_file_name, "w") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields_name)

        # writing the data rows
        csvwriter.writerows(rows)

    print("Inserted one payment record")


def mc_status_csv(transaction_id, transaction_status):

    today = datetime.datetime.now
    csv_file_name = "./sample_data/status.csv"

    # list of fields name for mc_status
    fields_name = ["DATA_CRE", "CORRELATION_ID", "BRCH", "ERROR_CODE"]
    rows = [[today(), transaction_id, "4500", transaction_status]]

    # writing to csv file
    with open(csv_file_name, "w") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields_name)

        # writing the data rows
        csvwriter.writerows(rows)
    print(os.system("ls"))
    print("Inserted one status record")


@step(
    "Add a transaction every <frequency> seconds for <duration> seconds in mc_payments and mc_status"
)
def add_a_transaction_every_seconds_for_seconds_in_the_new_tables(frequency, duration):
    t_end = end_time(duration)
    error = None
    try:
        while time.time() < t_end:
            transaction_id = random_tran_id()
            mc_payment_csv(transaction_id)
            mc_status_csv(transaction_id, "0000")
            print(os.system("sh ./scripts/liquibase_pay_insert.sh"))
            time.sleep(int(frequency))

    except (Exception, Error) as err:
        error = err
    finally:
        assert error is None, error
        print("Done")
