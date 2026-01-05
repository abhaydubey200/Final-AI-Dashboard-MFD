def validate_select_query(query: str) -> bool:
    """
    Allow only safe SELECT queries
    """
    q = query.strip().lower()
    return q.startswith("select") and "drop" not in q and "delete" not in q


def execute_query(conn, query: str):
    """
    Execute SELECT query and return cursor
    """
    cur = conn.cursor()
    cur.execute(query)
    return cur
