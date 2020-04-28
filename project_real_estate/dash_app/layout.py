import dash_core_components as dcc
import dash_html_components as html
import dash_table

from project_real_estate.constants import COLUMNS_TO_DISPLAY
from project_real_estate.dash_app.models import rent_model
from project_real_estate.db import sales_data


def _format_data(data):
    # Keep civic No., street and city
    data.full_address = data.full_address.apply(lambda x: "".join(x.split(",")[:2]))
    data.city = data.city.apply(lambda x: x.split("(")[0].strip())
    data = data.loc[:, COLUMNS_TO_DISPLAY]
    # Format numerical columns
    data["price"] = data.price.apply(lambda x: f"${x:,.0f}")
    data["predicted_rent_revenue"] = data.predicted_rent_revenue.apply(
        lambda x: f"${x:,.0f}"
    )
    data.rename(
        columns={
            "full_address": "Address",
            "city": "City",
            "price": "Price",
            "predicted_rent_revenue": "Predicted Rent Revenue",
            "url": "URL",
        },
        inplace=True,
    )
    return data


predicted_rent_revenue = rent_model.predict(sales_data)
sales_data_with_predictions = sales_data.join(predicted_rent_revenue, how="inner")
sales_data_display_with_predictions = _format_data(sales_data_with_predictions)


app_header = html.Div(
    [
        html.H1("Real Estate Investment Guru", id="app-title"),
        html.H3("A tool to help guide your investment decisions", id="app-subtitle"),
    ],
    id="app-header",
)


property_filter_elements = [
    html.P("Property filters", className="control-title"),
    html.P("What city do you want to look in?", className="control-label"),
    dcc.Dropdown(
        id="city_options",
        options=[
            {"label": city, "value": city}
            for city in sales_data_display_with_predictions.City.unique()
        ],
        multi=True,
        value=[],
        className="control",
    ),
]


property_input_elements = [
    html.P("Property parameters", className="control-title"),
    html.P("What is your downpayment budget?", className="control-label"),
    dcc.Slider(
        id="downpayment_budget_slider",
        min=10,
        max=500,
        step=10,
        marks={
            10: "$10K",
            100: "$100K",
            200: "$200K",
            300: "$300K",
            400: "$400K",
            500: "$500K",
        },
        # tooltip={"visible": True},
        className="control",
    ),
    html.P(
        "Other than [TO FILL IN] fees, what is the amount of other fees?",
        className="control-label",
    ),
    dcc.Slider(
        id="other_fees_rate",
        min=0,
        max=10,
        step=0.5,
        marks={0: "0%", 5: "5%", 10: "10%"},
        className="control",
    ),
    html.P("What is the tax rate on the property's income?", className="control-label"),
    dcc.Slider(
        id="income_tax_rate",
        min=0,
        max=20,
        step=0.5,
        marks={0: "0%", 10: "10%", 20: "20%"},
        className="control",
    ),
]

cash_flow_input_elements = [
    html.P("Cash flow parameters", className="control-title"),
    html.P("What is your yearly rent increase?", className="control-label"),
    dcc.Slider(
        id="rent_increase",
        min=0,
        max=5,
        step=0.1,
        value=2,
        marks={0: "0%", 5: "5%"},
        # tooltip={"visible": True},
        className="control",
    ),
    html.P("What is the yearly vacancy rate?"),
    dcc.Slider(
        id="vacancy_rate",
        min=0,
        max=20,
        step=1,
        value=4,
        marks={0: "0%", 20: "20%"},
        # tooltip={"visible": True},
        className="control",
    ),
]

mortgage_input_elements = [
    html.P("Mortgage parameters", className="control-title"),
    html.P("What is the interest rate on the mortgage?", className="control-label"),
    dcc.Slider(
        id="interest_rate_slider",
        min=0,
        max=10,
        value=8,
        step=0.01,
        marks={0: "0%", 5: "5%", 10: "10%"},
        # tooltip={"visible": True},
        className="control",
    ),
    html.P("How long is the amortization period?", className="control-label"),
    dcc.Input(
        id="amortization_period",
        type="number",
        placeholder="Amortization period",
        min=0,
        max=50,
        step=1,
        className="control control-input",
    ),
    html.P("When is the first year of repayment?", className="control-label"),
    dcc.Input(
        id="first_year_repayment",
        type="number",
        placeholder="First year of repayment",
        min=0,
        max=10,
        value=1,
        step=1,
        className="control control-input",
    ),
]

user_inputs = html.Div(
    [
        html.Div(property_filter_elements, className="pretty-container"),
        html.Div(property_input_elements, className="pretty-container"),
        html.Div(mortgage_input_elements, className="pretty-container"),
        html.Div(cash_flow_input_elements, className="pretty-container"),
    ],
    id="model-inputs",
)

reports_section = html.Div(
    [
        html.H2("Investment report", className="control-title"),
        html.P(
            f"By investing in this property, your discounted average ROI over the next 25 years is estimated "
            f"to be between {11.1} and {14.2}%, which represents net returns of ${670_100:,} to ${980_400:,}",
            id="reports-text",
        ),
    ],
    className="pretty-container",
    id="reports-section",
)


results_list = dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i} for i in sales_data_display_with_predictions.columns],
    data=[],
)
