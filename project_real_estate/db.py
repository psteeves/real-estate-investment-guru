import os

import pandas as pd
from sqlalchemy import create_engine


def pull_data(table_name, output_file=None, max_rows=10000):
    db_uri = os.environ["DB_URI"]
    engine = create_engine(db_uri)
    sql = f"SELECT * FROM {table_name}"
    if max_rows is not None:
        sql += f" LIMIT {max_rows};"

    data = pd.read_sql(sql=sql, con=engine)

    if output_file is not None:
        data.to_csv(open(output_file, "w"), index=False)
        print(f"Data written to {output_file}")

    return data
