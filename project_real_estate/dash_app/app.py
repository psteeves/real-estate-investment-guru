import dash
import dash_html_components as html
from dash.dependencies import Input, Output

from project_real_estate.constants import COLUMNS_TO_DISPLAY
from project_real_estate.dash_app.layout import (
    app_header,
    num_results_filter,
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
app.layout = html.Div(
    [app_header, user_inputs, reports_section, num_results_filter, results_list]
)


financial_model = TrivialFinancialModel()
rent_model = TrivialRentEstimator()


@app.callback(
    Output(component_id="forecast_horizon", component_property="max"),
    [Input(component_id="amortization_period", component_property="value"),],
)
def update_max_forecast_horizon(amortization_period):
    return amortization_period


@app.callback(
    Output(component_id="forecast_horizon", component_property="value"),
    [Input(component_id="forecast_horizon", component_property="max"),],
)
def update_value_forecast_horizon(max_value):
    return max_value


@app.callback(
    Output(component_id="table", component_property="data"),
    [
        Input(component_id="city", component_property="value"),
        Input(component_id="budget", component_property="value"),
        Input(component_id="year_built", component_property="value"),
        Input(component_id="downpayment", component_property="value"),
        Input(component_id="closing_fees", component_property="value"),
        Input(component_id="interest_rate", component_property="value"),
        Input(component_id="amortization_period", component_property="value"),
        Input(component_id="forecast_horizon", component_property="value"),
        Input(component_id="vacancy_rate", component_property="value"),
        Input(component_id="property_tax_rate", component_property="value"),
        Input(component_id="rent_increase", component_property="value"),
        Input(component_id="expense_ratio", component_property="value"),
        Input(component_id="yearly_reserves", component_property="value"),
        Input(component_id="num_results", component_property="value"),
    ],
)
def predict_roi(
    city_filters,
    budget,
    year_built_filter,
    downpayment,
    closing_fees,
    interest_rate,
    amortization,
    forecast_horizon,
    vacancy,
    property_tax_rate,
    rate_rent_increase,
    expense_ratio,
    yearly_reserves,
    num_results,
):
    if not city_filters:
        filtered_sales = sales_data_display_with_rent_predictions
    else:
        filtered_sales = sales_data_display_with_rent_predictions[
            sales_data_display_with_rent_predictions.City.isin(city_filters)
        ]

    sales_under_budget = filtered_sales[
        (filtered_sales.Price > budget[0]) & (filtered_sales.Price < budget[1])
    ]

    filtered_sales = sales_under_budget[
        (sales_under_budget.year_built > year_built_filter[0])
        & (sales_under_budget.year_built < year_built_filter[1])
    ]

    # Convert percentages to decimals
    downpayment /= 100
    closing_fees /= 100
    interest_rate /= 100
    vacancy /= 100
    property_tax_rate /= 100
    rate_rent_increase /= 100
    expense_ratio /= 100

    finance_model = SimpleFinancialModel(
        downpayment=downpayment,
        closing_fees=closing_fees,
        interest_rate=interest_rate,
        amortization=amortization,
        forecast_horizon=forecast_horizon,
        vacancy=vacancy,
        property_tax_rate=property_tax_rate,
        rate_rent_increase=rate_rent_increase,
        expense_ratio=expense_ratio,
        yearly_reserves=yearly_reserves,
    )
    prediction = finance_model.predict(filtered_sales).loc[:, COLUMNS_TO_DISPLAY]
    prediction = prediction.sort_values(by="ROE", ascending=False)
    prediction["ROE"] = prediction["ROE"].apply(lambda x: f"{x:.1%}")
    prediction["Cap Rate"] = prediction["Cap Rate"].apply(lambda x: f"{x:.1%}")
    prediction["Cash Return"] = prediction["Cash Return"].apply(lambda x: f"{x:.1%}")

    prediction["Initial Investment"] = prediction["Initial Investment"].apply(
        lambda x: f"{x:,.0f}"
    )

    prediction["Gross Revenue"] = prediction["Gross Revenue"].apply(
        lambda x: f"{x:,.0f}"
    )

    prediction["Net Income"] = prediction["Net Income"].apply(lambda x: f"{x:,.0f}")

    prediction["Net Cash"] = prediction["Net Cash"].apply(lambda x: f"{x:,.0f}")

    prediction["Price"] = prediction["Price"].apply(lambda x: f"{x:,.0f}")

    return prediction.iloc[:num_results].to_dict("rows")


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
