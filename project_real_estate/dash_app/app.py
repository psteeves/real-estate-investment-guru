import dash
import dash_html_components as html
from dash.dependencies import Input, Output

from project_real_estate.constants import COLUMNS_TO_DISPLAY, MAX_NUM_RESULTS
from project_real_estate.dash_app.layout import (
    app_header,
    reports_section,
    results_list,
    sales_data_display_with_rent_predictions,
    user_inputs,
)
from project_real_estate.models.financial_model import (
    SimpleFinancialModel,
    TrivialFinancialModel,
)
from project_real_estate.models.rent_estimator import TrivialRentEstimator

app = dash.Dash(__name__)
app.layout = html.Div([app_header, user_inputs, reports_section, results_list])


financial_model = TrivialFinancialModel()
rent_model = TrivialRentEstimator()


@app.callback(
    Output(component_id="table", component_property="data"),
    [
        Input(component_id="city", component_property="value"),
        Input(component_id="budget", component_property="value"),
        Input(component_id="downpayment", component_property="value"),
        Input(component_id="closing_fees", component_property="value"),
        Input(component_id="interest_rate", component_property="value"),
        Input(component_id="amortization_period", component_property="value"),
        Input(component_id="vacancy_rate", component_property="value"),
        Input(component_id="rent_increase", component_property="value"),
        Input(component_id="expense_ratio", component_property="value"),
        Input(component_id="yearly_reserves", component_property="value"),
    ],
)
def predict_roi(
    city_filters,
    budget,
    downpayment,
    closing_fees,
    interest_rate,
    amortization,
    vacancy,
    rate_rent_increase,
    expense_ratio,
    yearly_reserves,
):
    if not city_filters:
        sales_by_city = sales_data_display_with_rent_predictions
    else:
        sales_by_city = sales_data_display_with_rent_predictions[
            sales_data_display_with_rent_predictions.City.isin(city_filters)
        ]

    sales_under_budget = sales_by_city[sales_by_city.Price < budget]

    finance_model = SimpleFinancialModel(
        downpayment=downpayment,
        closing_fees=closing_fees,
        interest_rate=interest_rate,
        amortization=amortization,
        vacancy=vacancy,
        rate_rent_increase=rate_rent_increase,
        expense_ratio=expense_ratio,
        yearly_reserves=yearly_reserves,
    )
    prediction = finance_model.predict(sales_under_budget).loc[:, COLUMNS_TO_DISPLAY]
    prediction = prediction.sort_values(
        by="ROE", ascending=False
    )
    prediction["ROE"] = prediction[
        "ROE"
    ].apply(lambda x: f"{x:.1%}")

    prediction["Cash Return"] = prediction["Cash Return"].apply(
        lambda x: f"{x:.1%}")

    prediction["Initial Investment"] = prediction[
        "Initial Investment"
    ].apply(lambda x: f"{x:,.0f}")

    prediction["Gross Revenue"] = prediction[
        "Gross Revenue"
    ].apply(lambda x: f"{x:,.0f}")

    prediction["Net Income"] = prediction[
        "Net Income"
    ].apply(lambda x: f"{x:,.0f}")

    prediction["Net Cash"] = prediction[
        "Net Cash"
    ].apply(lambda x: f"{x:,.0f}")

    prediction["Price"] = prediction[
        "Price"
    ].apply(lambda x: f"{x:,.0f}")

    return prediction.iloc[:MAX_NUM_RESULTS].to_dict("rows")


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
