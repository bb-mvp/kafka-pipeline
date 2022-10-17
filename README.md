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

- Create the [PostgreSQL database on AWS RDS](https://aws.amazon.com/rds/postgresql/)
 
- Verify you can connect to the database
  - You can do this using any PostgreSQL client

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
