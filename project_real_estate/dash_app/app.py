import dash
import dash_html_components as html
from dash.dependencies import Input, Output

from project_real_estate.dash_app.layout import (
    app_header,
    model_inputs,
    reports_section,
    results_list,
)
from project_real_estate.models.financial_model import TrivialFinancialModel
from project_real_estate.models.rent_estimator import TrivialRentEstimator

app = dash.Dash(__name__)
app.layout = html.Div([app_header, model_inputs, reports_section, results_list])


financial_model = TrivialFinancialModel()
rent_model = TrivialRentEstimator()


@app.callback(
    Output(component_id="reports-text", component_property="children"),
    [Input(component_id="downpayment_budget_slider", component_property="value")],
)
def update_report(input_value):
    return rent_model(input_value) + financial_model(input_value)


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
