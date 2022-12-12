drop table bdol_tx;
drop table mc_payments;
drop table mc_status;
drop table transaction;
drop table databasechangelog;
drop table databasechangeloglock;
drop table debezium_heartbeat;


truncate table mc_status;
truncate table mc_payments;


select * from mc_payments;

select * from mc_status;
