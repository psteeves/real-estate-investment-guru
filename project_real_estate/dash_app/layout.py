import dash_core_components as dcc
import dash_html_components as html
import dash_table

from project_real_estate.constants import COLUMNS_TO_DISPLAY, MAX_NUM_RESULTS
from project_real_estate.dash_app.models import rent_model
from project_real_estate.db import sales_data


def _format_data(data):
    # Keep civic No., street and city
    data.full_address = data.full_address.apply(lambda x: "".join(x.split(",")[:2]))
    data.city = data.city.apply(lambda x: x.split("(")[0].strip())

    # Round dollar amounts
    data.price = data["price"].apply(lambda x: round(x, 0))
    data.predicted_rent_revenue = data["predicted_rent_revenue"].apply(
        lambda x: round(x, 0)
    )

    # Make URL markdown
    data.url = data.url.apply(lambda x: "[Centris Link](" + x + ")")
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
sales_data_with_rent_predictions = sales_data.join(predicted_rent_revenue, how="inner")
sales_data_display_with_rent_predictions = _format_data(
    sales_data_with_rent_predictions
)


app_header = html.Div(
    [
        html.H1("Real Estate Investment Guru", id="app-title"),
        html.H3("A tool to help guide your investment decisions", id="app-subtitle"),
    ],
    id="app-header",
)


property_filter_elements = [
    html.P("Property filters", className="control-title"),
    html.P("City", className="control-label"),
    dcc.Dropdown(
        id="city",
        options=[
            {"label": city, "value": city}
            for city in sales_data_display_with_rent_predictions.City.unique()
        ],
        multi=True,
        value=[],
        className="control",
    ),
    html.P("Budget", className="control-label"),
    dcc.Slider(
        id="budget",
        min=0,
        max=1000000,
        step=50000,
        value=500000,
        marks={
            0: "$0",
            250000: "$250K",
            500000: "$500K",
            750000: "$750K",
            1000000: "$1M",
        },
        className="control",
    ),
]


cash_flow_input_elements = [
    html.P("Cash flow parameters", className="control-title"),
    html.P("Yearly rent increase", className="control-label"),
    dcc.Slider(
        id="rent_increase",
        min=0,
        max=0.1,
        step=0.01,
        value=0.02,
        marks={0: "0%", 0.1: "10%"},
        className="control",
    ),
    html.P("Expense ratio w.r.t gross revenue", className="control-label",),
    dcc.Slider(
        id="expense_ratio",
        min=0,
        max=0.5,
        step=0.05,
        value=0.2,
        marks={0: "0%", 0.25: "25%", 0.5: "50%"},
        className="control",
    ),
    html.P("Yearly cash reserves", className="control-label",),
    dcc.Slider(
        id="yearly_reserves",
        min=0,
        max=10000,
        step=1000,
        value=1000,
        marks={0: "1,000$", 5000: "5,000$", 10000: "10,000$"},
        className="control",
    ),
    html.P("Vacancy rate"),
    dcc.Slider(
        id="vacancy_rate",
        min=0,
        max=0.2,
        step=0.01,
        value=0.04,
        marks={0: "0%", 0.1: "10%", 0.2: "20%"},
        className="control",
    ),
]


investment_input_elements = [
    html.P("Investment parameters", className="control-title"),
    html.P("Downpayment", className="control-label"),
    dcc.Slider(
        id="downpayment",
        min=0,
        max=0.3,
        value=0.1,
        step=0.05,
        marks={0: "0%", 0.1: "10%", 0.2: "20%", 0.3: "30%"},
        className="control",
    ),
    html.P("Mortgage interest rate", className="control-label"),
    dcc.Slider(
        id="interest_rate",
        min=0,
        max=0.1,
        value=0.08,
        step=0.001,
        marks={0: "0%", 0.05: "5%", 0.1: "10%"},
        className="control",
    ),
    html.P("Amortization period", className="control-label"),
    dcc.Input(
        id="amortization_period",
        type="number",
        placeholder="Amortization period",
        min=0,
        max=50,
        step=5,
        value=20,
        className="control control-input",
    ),
    html.P("Total closing fees", className="control-label",),
    dcc.Slider(
        id="closing_fees",
        min=0,
        max=0.1,
        step=0.01,
        value=0.02,
        marks={0: "0%", 0.05: "5%", 0.1: "10%"},
        className="control",
    ),
]

user_inputs = html.Div(
    [
        html.Div(property_filter_elements, className="pretty-container"),
        html.Div(investment_input_elements, className="pretty-container"),
        html.Div(cash_flow_input_elements, className="pretty-container"),
    ],
    id="model-inputs",
)

reports_section = html.Div(
    [
        html.H2("Investment report", className="control-title"),
        html.P(
            f"Top {MAX_NUM_RESULTS} properties that fit your requirements, with respect to Return on Equity (average over amortization period).",
            id="reports-text",
        ),
    ],
    className="pretty-container",
    id="reports-section",
)

results_list = dash_table.DataTable(
    id="table",
    columns=[
        {"name": i, "id": i, "type": "text", "presentation": "markdown"}
        for i in COLUMNS_TO_DISPLAY
    ],
    data=[],
    style_cell_conditional=[
        {"if": {"column_id": c}, "textAlign": "left"}
        for c in ["Address", "City", "URL"]
    ],
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
    ],
    style_as_list_view=True,
    style_cell={"padding": "15px"},
    style_header={"fontWeight": "bold"},
)
