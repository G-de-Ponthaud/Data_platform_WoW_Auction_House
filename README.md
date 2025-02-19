# Data_platform_WoW_Auction_House
Small data platform that take auction form the Wow API and make an history of cleaned data.

# 1- Requirements
For this project, we will use the following tools :
  - Airbyte
  - Snowflake
  - dbt
  - Airflow

Therefore, before starting, we need to install Airbyte, dbt Core, and Airflow.
For Airbyte, the simplest method is to use a Docker container, which can be built with the command 

    docker-compose up

For dbt, you will need to execute the command:

    pip install -r requirements.txt

Finally, Airflow can be installed using the commands:

    pip install apache-airflow
    pip install apache-airflow-providers-snowflake

Additionally, you will need to create a Snowflake instance. This can be done by using the [free trial version](https://signup.snowflake.com/) available for 30 days (no credit card required).

# A) Airbyte
To create a custom connector on Airbyte, you first need to start your Docker container with `docker-compose up`. Then, navigate to [localhost:8000](localhost:8000) and log in using your credentials (by default, the username is `airbyte` and the password is `password`).

Once logged in, the first step will be to create a new source by clicking on `sources` followed by `Need to build your own source?`and start from scratch.

In the window that will open, you need to enter the base of the URL. In our case, it is :

    https://eu.api.blizzard.com/data
Also, you will define the Authentification Method to OAuth and choose client_credentials for the Grant Type.

We can now create a stream by clicking and the + next to streams(). There, we define the neame of the stream and the URL PATH :
    
    /wow/auctions/commodities

We will also need to declare the query parameters to :

locale = en_US
namespace = dynamic-eu

We can now test and create the source.

After that you have to click on the connections tab and click on the + button then custom and select the source you just create. Define your develop.battle.net credentials.
After the credentials check, click on `Airbyte Connectors` and select `Snowflake`.
Enter your snowflake Credentials and change Authorization Method to Username and Password and enter your Snowflake Password.
Test the destination. 
In the next window choose `Replicate Source` and click on next.
Set the frequency that you want (not under 1h) and click on `Finish & Sync`.

The airbyte pipeline is now create.

# B) dbt

The following dbt folder contains models, macros, test, snapshots and sources.

Before run dbt, you should create a .env file with all your snowflake credentials and use :
    
    . .env

The idea of the architecture is to ingest raw data and deserialized it before split in into item tables to facilitate future joins for exploit the data.

# C) Airflow

Airflow is used here for orchestrate and automate the execution of dbt and ingestion of the item.csv file.

The first things to do is to use the command to initialize the airflow db and create a airflow user :

    airflow db init
    airflow users create \
    --username admin \
    --password admin \
    --role Admin \
    --email admin@example.com \
    --firstname Admin \
    --lastname User

Next, if you want to use airflow in your project folder, you need to edit the different paths of the `airflow.cfg` file to point to your project folder ( ex: `/home/username/project_folder/airflow/` ).

You can now run the commands to launch airflow with : 

    airflow webserver --port 8080
    airflow scheduler

Once you are log in using the credential of the airflow user we created before (admin / admin), you car create a connexion to your snowflake account and create variables to pass the different credentials needed to your executions (snowflake and battle.net apis).

You have now to create the different dags and let them run.
