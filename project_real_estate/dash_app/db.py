import pandas as pd
from sqlalchemy import create_engine
import os


def pull_data(table_name):
    db_uri = os.environ["DB_URI"]
    engine = create_engine(db_uri)
    sql = f"SELECT * FROM {table_name};"
    data = pd.read_sql(sql=sql, con=engine)
    return data
