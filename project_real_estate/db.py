import os

import pandas as pd
from sqlalchemy import create_engine

from project_real_estate.constants import COLUMNS_TO_DISPLAY


def _pull_data(table_name):
    db_uri = os.environ["DB_URI"]
    engine = create_engine(db_uri)
    sql = f"SELECT * FROM {table_name};"
    data = pd.read_sql(sql=sql, con=engine)
    return _format_data(data)


def _format_data(table):
    # Remove neighborhood in parentheses
    table.city = table.city.apply(lambda x: x.split("(")[0].strip())
    return table


def _format_data_display(data):
    # Keep civic No., street and city
    data.full_address = data.full_address.apply(lambda x: "".join(x.split(",")[:2]))
    data = data.loc[:, COLUMNS_TO_DISPLAY]
    data.rename(
        columns={
            "full_address": "Address",
            "city": "City",
            "price": "Price",
            "url": "URL",
        },
        inplace=True,
    )
    return data


sales_data = _pull_data("sales")
sales_data_display = _format_data_display(sales_data)
