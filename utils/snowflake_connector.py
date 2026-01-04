import snowflake.connector
import pandas as pd
from config import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_USER,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_ROLE
)


def connect_snowflake(
    account,
    user,
    password,
    warehouse,
    database,
    schema,
    role
):
    return snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role
    )


def fetch_table(conn, database, schema, table):
    query = f"SELECT * FROM {database}.{schema}.{table}"
    return pd.read_sql(query, conn)
