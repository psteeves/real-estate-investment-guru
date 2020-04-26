import argparse
import os

import pandas as pd
from sqlalchemy import create_engine


def _pull_data(table_name, output_file):
    db_uri = os.environ["DB_URI"]
    engine = create_engine(db_uri)
    sql = f"SELECT * FROM {table_name};"
    data = pd.read_sql(sql=sql, con=engine)
    data.to_csv(open(output_file, "w"))
    print(f"Data written to {output_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", required=True, help="Table name to pull.")
    parser.add_argument(
        "-o", "--output-file", required=True, help="File to output data to."
    )
    args = parser.parse_args()

    _pull_data(args.table, args.output_file)


if __name__ == "__main__":
    main()
