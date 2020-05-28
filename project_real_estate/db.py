import os

import pandas as pd
from sqlalchemy import create_engine


def _pull_data(table_name, max_rows=30000):
    db_uri = os.environ["DB_URI"]
    engine = create_engine(db_uri)
    sql = f"SELECT * FROM {table_name} LIMIT {max_rows};"
    data = pd.read_sql(sql=sql, con=engine)
    return data


sales_data = _pull_data("sales")
