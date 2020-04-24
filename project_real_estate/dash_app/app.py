import dash
import dash_html_components as html
from dash.dependencies import Input, Output

from project_real_estate.constants import MAX_NUM_RESULTS
from project_real_estate.dash_app.layout import (
    app_header,
    reports_section,
    results_list,
    user_inputs,
)
from project_real_estate.db import sales_data_display
from project_real_estate.models.financial_model import TrivialFinancialModel
from project_real_estate.models.rent_estimator import TrivialRentEstimator

app = dash.Dash(__name__)
app.layout = html.Div([app_header, user_inputs, reports_section, results_list])


financial_model = TrivialFinancialModel()
rent_model = TrivialRentEstimator()


@app.callback(
    Output(component_id="table", component_property="data"),
    [Input(component_id="city_options", component_property="value")],
)
def update_report(city_filters):
    if not city_filters:
        return sales_data_display.iloc[:MAX_NUM_RESULTS, :].to_dict("rows")
    return (
        sales_data_display[sales_data_display.City.isin(city_filters)]
        .iloc[:MAX_NUM_RESULTS, :]
        .to_dict("rows")
    )


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
