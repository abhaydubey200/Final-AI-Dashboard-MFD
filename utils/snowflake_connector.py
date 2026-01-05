import snowflake.connector

def get_snowflake_connection(
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
