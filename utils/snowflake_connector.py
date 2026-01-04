import snowflake.connector
import pandas as pd

def fetch_snowflake_data(
    account,
    user,
    password,
    warehouse,
    database,
    schema,
    table
):
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    query = f"SELECT * FROM {table}"
    df = pd.read_sql(query, conn)

    conn.close()
    return df
