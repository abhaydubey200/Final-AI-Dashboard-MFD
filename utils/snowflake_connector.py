import snowflake.connector
import pandas as pd


def get_snowflake_connection(creds: dict):
    """
    Create and return a Snowflake connection
    """
    return snowflake.connector.connect(
        account=creds["account"],
        user=creds["user"],
        password=creds["password"],
        warehouse=creds["warehouse"],
        database=creds["database"],
        schema=creds["schema"],
        role=creds["role"],
    )


def fetch_table_df(conn, database, schema, table):
    """
    Load full Snowflake table into Pandas DataFrame
    """
    query = f'SELECT * FROM "{database}"."{schema}"."{table}"'
    return pd.read_sql(query, conn)
