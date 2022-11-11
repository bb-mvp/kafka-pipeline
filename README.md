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
      - you can choose your own password if you prefer that to an auto generated one
      - choose "Yes" for Public access
    - Finally click on the "Create database" button at the bottom of the page
  - [Add an inbound rule allowing connections to Postgres](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html#USER_ConnectToPostgreSQLInstance.Troubleshooting-AccessRules):
    - Go to the [databases page](https://console.aws.amazon.com/rds/home#databases:)
    - Click on your database
    - On the "Connectivity & security" tab, click on the VPC security group (under "Security"), to take
      you to the VPC section of AWS
    - Click on "[Security Groups](https://console.aws.amazon.com/ec2/v2/home#SecurityGroups:)" in the left menu
    - Click on the "Inbound rules" tab at the bottom of the page
    - Click on "Edit inbound rules"
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
  - `AWS_DATABASE_HOST` (this is the endpoint in the "Connectivity & security" tab of your
     database, found by navigating to the [databases page](https://console.aws.amazon.com/rds/home#databases:))
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


### Stream the AWS data into Kafka (Confluent Cloud)

We are using [Confluent Cloud](https://www.confluent.io/confluent-cloud) as our Kafka platform for this proof of
concept, as it is a fully-managed platform which makes it very easy to get started with.

#### Setup your Confluent Cloud account

1. Sign up via https://www.confluent.io/confluent-cloud/tryfree/
3. Add promo codes to add to your free credit:
   - ask a [repository maintainer](.github/CODEOWNERS) for the promo codes you need to add
   - go to Confluent's [payments page](https://confluent.cloud/settings/billing/payment) and add the promo codes, one
     by one
   - this should give you enough credit to last 3 months

#### Create a Kafka cluster on Confluent Cloud

- Follow step 1 (step 1 only, don't continue to step 2)
  [of Confluent's documentation](https://docs.confluent.io/cloud/current/get-started/index.html#step-1-create-a-ak-cluster-in-ccloud)

#### Add a Postgres CDC Source connector to your Kafka cluster

Background reading: [Postgres CDC Source connector documentation](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html#postgresql-cdc-source-connector-debezium-for-ccloud)

1. Navigate to your new cluster on Confluent Cloud
2. Click on "Connectors" on the left menu
3. Choose "Postgres CDC Source"
4. Keep "Global access" selected and click on "Generate API key & download"
5. Give your API credentials a name
6. On the configuration input form, enter:
   - Database name: `postgres`
   - Database server name: `mvp` (or anything you like. It will become the prefix for your Kafka topics)
   - SSL mode: `require`
   - Database hostname: the endpoint in the "Connectivity & security" tab of your
     AWS database, on the [AWS databases page](https://console.aws.amazon.com/rds/home#databases:)
   - Database port: `5432`
   - Database username: `postgres`
   - Database password: your AWS Postgres database password
7. Click on "Continue"
8. Choose `JSON` as both the "Output Kafka record value" and "Output Kafka record key" formats
9. Expand the "Show advanced configurations" dropdown and enter the following:
   - JSON output decimal format: `NUMERIC`
   - Plugin name: `pgoutput`
   - Tables included: `public.transaction`
   - Decimal handling mode: `string`
10. Click on "Continue"
11. Click on "Continue" on the "Connector sizing" page
12. Click on "Continue" on the "Review and launch page"
13. Wait a minute or so for the connector to be provisioned

#### Stream data into Kafka via the Postgres CDC Source connector

This is very straightforward:

1. [Add example bank transactions to your AWS database](#add-example-bank-transactions-into-your-aws-database-via-the-github-actions-workflow)
2. On Confluent Cloud, navigate to your cluster and click on "Topics" on the left menu
3. You will see that a `<your-prefix>.public.transaction` topic has been added
4. If you click on the topic and then the "Messages" tab, you can see the messages by specifying the
   offset as `0 / Partition: 0`

   Also, if you then kick off another GitHub Actions workflow run to add more bank transactions to your
   AWS database, if you go to the "Messages" tab of your Kakfa topic and keep the page open, you will see
   the bank transactions appear in Kakfa in realtime.

#### Delete your AWS database to avoid paying for consuming too much storage

Under certain conditions the AWS database is consuming storage very quickly after connecting the database to Kafka via Postgres CDC. This can exhaust AWS's free monthly 20GB limit and lead to credit card charges.

We have a [GitHub issue for this](https://github.com/bb-mvp/kafka-pipeline/issues/30), and all contributors are very
welcome to try to solve it.

Until this issue is solved the recommended course of action is to delete the AWS database after successfully verifying you have the CDC connection between Kafka and the database working.  It looks like it takes several hours for the 20GB to be
consumed, but it's best to delete (or at least pause) the AWS database as soon as you are finished working with it.
(Pausing it is great, but has the important caveat that it will automatically be restarted again after 7 days, which is a
little dangerous compared to deleting it).





