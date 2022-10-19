# kafka-pipeline
Kakfa data pipeline streaming real-time data from a relational database

## Overview

The pipeline streams data from an [AWS RDS PostgreSQL database](https://aws.amazon.com/rds/postgresql/) into a 
[Kafka](https://kafka.apache.org/) cluster on [Confluent Cloud](https://www.confluent.io/confluent-cloud/), using
Change Data Capture (CDC) via [Debezium](https://debezium.io).

## Setting up the pipeline

### Create and populate a PostgreSQL database on AWS RDS

#### Create a PostgreSQL database on AWS RDS

- Sign up for a new AWS account with 12 month free trial

- Change your region to `eu-west-1` (Ireland) via the top-right navigation
  (it can be any region really, so feel free to choose another one if you prefer)

- Create and setup the [PostgreSQL database on AWS RDS](https://aws.amazon.com/rds/postgresql/)
  - Create the database
    - Go to the [RDS homepage on the AWS console](https://console.aws.amazon.com/rds/home)
    - Click "Create database"
    - Choose "Standard create"
    - Choose "PostgreSQL" as the Engine type
    - keep the default version `13.x` of Postgres (we have tested that the pipeline works with `14` too, but easiest
      to keep with the default)
    - Make sure you choose the Free tier template
    - Keep all the other defaults as they are, apart from:
      - choosing whichever name you like for the database
      - choose "Yes" for Public access
  - [Add an inbound rule allowing connections to Postgres](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html#USER_ConnectToPostgreSQLInstance.Troubleshooting-AccessRules):
    - Go to the [databases page](https://console.aws.amazon.com/rds/home#databases:)
    - Click on your database
    - On the "Connectivity & security" tab, click on the VPC security group (under "Security"), to take
      you to the [Security Groups page](https://console.aws.amazon.com/ec2/v2/home#SecurityGroups:)
    - At the bottom of the Security Groups page, click on "Edit inbound rules"
    - Add a new rule with the Type being `PostgreSQL` and a Custom Source of `0.0.0.0/0`

  - Verify you can connect to the database
      - You can do this using any PostgreSQL client
  - Turn on logical replication and apply it to your new database (needed for Change Data Capture to Kafka)
    - Go to the [parameter groups page on AWS](https://console.aws.amazon.com/rds/home#parameter-groups:)
    - Click on "create parameter group"
    - choose `postgres13` as the Parameter group family (matching the version 13 that we installed above)
    - call your new group `cdc-parameter-group`
    - click on "Create"
    - click on your newly created `cdc-parameter-group`
    - search for `rds.logical_replication`
    - click on "Edit parameters"
    - change the value of "rds.logical_replication" to "1"
    - click on "Save changes"
    - click on "Databases" on the left navigation menu and click on your database
    - click on the "Modify" button at the top right of the page
    - Scroll down to the "Additional configuration" section and expand it if necessary
    - Change the "DB parameter group" to the `cdc-parameter-group` parameter group you just created
    - Scroll down to the bottom and click the "Continue" button
    - Choose "Apply immediately"
    - Click "Modify DB instance"
    - NB it will take a few minutes for the change to be applied to the instance, and then you have to reboot
      (by navigating to `Actions` -> `Reboot`)
    - Verify logical replication has been successfully configured by running this query in whichever PostgreSQL
      client you are using, and checking that the returned `wal_level` is `logical`:

      `SELECT name,setting FROM pg_settings WHERE name IN ('wal_level','rds.logical_replication');`

#### Store your AWS PostgreSQL connection details as secrets on GitHub

- Create a [GitHub environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) on this repository, with the name being your GitHub username

- Add the AWS PostgreSQL connection details as
[environment secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-an-environment) to your environment

  The secrets you need to add are:
  - `AWS_DATABASE_HOST`
  - `AWS_DATABASE_NAME` (this will be `postgres`)
  - `AWS_DATABASE_PASSWORD`
  - `AWS_DATABASE_PORT` (this will be `5432`)
  - `AWS_DATABASE_USERNAME` (this will be `postgres`)

#### Add example bank transactions into your AWS database via the GitHub Actions workflow

1. Click on the [Actions](https://github.com/bb-mvp/kafka-pipeline/actions) tab for this GitHub repository
2. Click on the [`Add transactions on AWS`](https://github.com/bb-mvp/kafka-pipeline/actions/workflows/aws_add_transactions.yml) workflow
3. Click on `Run workflow` (on the right of the screen)
4. Enter your GitHub username as prompted
5. Verify that the workflow completes successfully:
   - Check the workflow result via the GitHub Actions UI
   - Use your PostgreSQL client to verify that your AWS database has new transactions in the `transaction` table

   NB You can run this workflow as often as you like, to add more data whenever you want to.


### Stream the AWS data into Kafka

- To Do: complete this documentation
