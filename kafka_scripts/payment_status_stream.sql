CREATE OR REPLACE STREAM "mc_status" (CORRELATION_ID STRING, ERROR_CODE STRING)
  WITH (kafka_topic='mvp.public.mc_status', partitions=1, value_format='JSON');

CREATE OR REPLACE STREAM "mc_payments" (BFO_TRANSACTION_ID STRING, CORRELATION_ID STRING, SOURCE_ACCOUNT STRING, SOURCE_ACCOUNT_CURRENCY STRING, SOURCE_ACCOUNT_OWNERID STRING,
   TARGET_ACCOUNT STRING, TARGET_ACCOUNT_CURRENCY STRING, TARGET_ACCOUNT_OWNERID STRING, TARGET_ACCOUNT_OWNER_NAME STRING, 
   TRANSACTION_AMOUNT STRING, TRANSACTION_CURRENCY STRING, TRANSACTION_DESCRIPTION STRING, TRANSACTION_VALUEDATE DATE, TRANSACTION_TYPE STRING )
  WITH (kafka_topic='mvp.public.mc_payments', partitions=1, value_format='JSON');

CREATE OR REPLACE STREAM "transactions"
  WITH (kafka_topic='transactions', partitions=1, value_format='JSON')
  AS SELECT P.BFO_TRANSACTION_ID AS TRANSACTION_ID, P.CORRELATION_ID as CORRELATION_ID, P.SOURCE_ACCOUNT AS SOURCE_ACCOUNT, P.TARGET_ACCOUNT AS DESTINATION_ACCOUNT, 
  P.TRANSACTION_AMOUNT AS AMOUNT, P.TRANSACTION_CURRENCY AS TRANSACTION_CURRENCY, P.TRANSACTION_DESCRIPTION AS DESCRIPTION, P.TRANSACTION_VALUEDATE AS BOOKING_DATE, 
  P.TRANSACTION_TYPE as type, 'D' as CREDIT_DEBIT, 'IBT' as TYPE_GROUP, P.SOURCE_ACCOUNT_OWNERID as CUSTOMER_ID,
  T.ERROR_CODE AS STATUS FROM "mc_status" T INNER JOIN "mc_payments" P
    WITHIN 365 DAY GRACE PERIOD 365 DAYS
  ON T.CORRELATION_ID = P.CORRELATION_ID;