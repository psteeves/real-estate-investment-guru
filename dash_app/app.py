from dash_app.layout import app_header, model_inputs, reports_section
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
from models.financial_model import TrivialFinancialModel
from models.rent_estimator import TrivialRentEstimator

app = dash.Dash(__name__)


app.layout = html.Div(
    [
        app_header,
        model_inputs,
        reports_section,
    ]
)


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
