import dash_core_components as dcc
import dash_html_components as html
import dash_table

from project_real_estate.constants import COLUMNS_TO_DISPLAY
from project_real_estate.dash_app.models import rent_model
from project_real_estate.db import pull_data

sales_data = pull_data("latest_sales", max_rows=None)
predicted_rent_revenue = rent_model.predict(sales_data)
sales_data_with_rent_predictions = sales_data.join(predicted_rent_revenue, how="inner")

oldest_year = int(sales_data_with_rent_predictions.year_built.min())
lowest_price = int(sales_data_with_rent_predictions.price.min())
highest_price = int(sales_data_with_rent_predictions.price.max())


app_header = html.Div(
    [
        html.H1("Real Estate Investment Guru", id="app-title"),
        html.H3(
            "A tool to help you find profitable investment opportunities",
            id="app-subtitle",
        ),
    ],
    id="app-header",
)


property_filter_elements = [
    html.P("About the App", className="control-title"),
    html.P(
        """ This App helps you quickly find the best investment opportunities by continually
    scanning the web for profitable properties, based on your requirements. The app will analyze 
    your preferred property types, predict potential rent revenue, and return the top investment
    opportunities based on Return on Equity."""
    ),
    html.P("Property filters", className="control-title"),
    html.P("City", className="control-label"),
    dcc.Dropdown(
        id="city",
        options=[
            {"label": city, "value": city}
            for city in sales_data_with_rent_predictions.city.unique()
        ],
        multi=True,
        value=[],
        className="control",
    ),
    html.P("Budget", className="control-label"),
    dcc.RangeSlider(
        id="budget",
        min=lowest_price,
        max=highest_price,
        step=100000,
        value=[lowest_price, highest_price],
        marks={
            0: "$0",
            5000000: "$5M",
            10000000: "10M",
            15000000: "15M",
            20000000: "20M",
            25000000: "25M",
        },
        className="control",
    ),
    html.P("Year built", className="control-label"),
    dcc.RangeSlider(
        id="year_built",
        min=oldest_year,
        max=2020,
        step=1,
        value=[1970, 2020],
        className="control",
        marks={value: f"{value}" for value in range(oldest_year, 2020, 20)},
    ),
]


cash_flow_input_elements = [
    html.P("Cash flow parameters", className="control-title"),
    html.P("Property tax rate", className="control-label"),
    dcc.Input(
        id="property_tax_rate",
        type="number",
        placeholder="Property tax rate",
        min=0.0,
        max=5.0,
        step=0.1,
        value=1.0,
        className="control control-input",
    ),
    html.P("Yearly rent increase", className="control-label"),
    dcc.Input(
        id="rent_increase",
        type="number",
        placeholder="Yearly rent increase",
        min=0.0,
        max=10.0,
        step=0.1,
        value=0.0,
        className="control control-input",
    ),
    html.P(
        "Expenses as percentage of yearly gross revenue *", className="control-label",
    ),
    dcc.Input(
        id="expense_ratio",
        type="number",
        placeholder="Expense Ratio",
        min=0,
        max=50,
        step=1,
        value=20,
        className="control control-input",
    ),
    html.P("Yearly cash reserves", className="control-label",),
    dcc.Input(
        id="yearly_reserves",
        type="number",
        placeholder="Yearly cash reserves",
        min=0,
        max=1000000,
        step=5000,
        value=0,
        className="control control-input",
    ),
    html.P("Yearly vacancy rate"),
    dcc.Input(
        id="vacancy_rate",
        type="number",
        placeholder="Vacancy rate",
        min=0.0,
        max=20.0,
        step=1.0,
        value=3.0,
        className="control control-input",
    ),
    html.Br(),
    html.P(
        "* Expense ratio assumed for buildings 10 years old or newer. Multiplied by 1.5 for older buildings.",
        style={"fontSize": 11},
    ),
]


investment_input_elements = [
    html.P("Deal parameters", className="control-title"),
    html.P("Downpayment (%)", className="control-label"),
    dcc.Input(
        id="downpayment",
        type="number",
        placeholder="Downpayment",
        min=5,
        max=20,
        step=5,
        value=15,
        className="control control-input",
    ),
    html.P("Mortgage interest rate (%)", className="control-label"),
    dcc.Input(
        id="interest_rate",
        type="number",
        placeholder="Interest rate",
        min=0,
        max=20,
        step=0.1,
        value=3,
        className="control control-input",
    ),
    html.P("Closing fees as % of purchase price", className="control-label"),
    dcc.Input(
        id="closing_fees",
        type="number",
        placeholder="Closing fees",
        min=0,
        max=5,
        step=0.5,
        value=2,
        className="control control-input",
    ),
    html.P("Amortization period", className="control-label"),
    dcc.Slider(
        id="amortization_period",
        min=0,
        max=25,
        step=5,
        value=25,
        marks={
            0: "0yrs",
            5: "5yrs",
            10: "10yrs",
            15: "15yrs",
            20: "20yrs",
            25: "25yrs",
        },
        className="control",
    ),
    html.P("Investment forecast horizon", className="control-label"),
    dcc.Slider(
        id="forecast_horizon",
        min=0,
        max=20,
        step=5,
        value=20,
        marks={0: "0yrs", 5: "5yrs", 10: "10yrs", 15: "15yrs", 20: "20yrs",},
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
            f"The below report shows the top properties that fit your requirements, "
            f"sorted by Return on Equity (averageed over the amortization period).",
            id="reports-text",
        ),
        html.P(
            f"The App's financial model takes the filtered properties and predicts their potential gross rental "
            f"revenue by analyzing comparable rental market data in real-time. "
            f"60% of properties' true rental price fall within 10% of our predicted rental revenue. "
            f"Once the potential gross revenue is estimated, the App factors in various cash flow components "
            f"(such as mortgage insurance premiums, closing fees, capital expenses, etc.) to establish an estimated "
            f"average yearly Return on Equity over the loan amortization period.",
            id="reports-text-2",
        ),
    ],
    className="pretty-container",
    style={"margin-bottom": "40px"},
    id="reports-section",
)

num_results_filter = html.Div(
    [
        html.P("Number of results to show:"),
        dcc.Input(
            id="num_results",
            type="number",
            placeholder="Number of Search Results",
            min=1,
            max=100,
            step=1,
            value=20,
            className="control control-input",
        ),
    ],
)

results_list = dash_table.DataTable(
    id="table",
    columns=[
        {"name": i, "id": i, "type": "text", "presentation": "markdown"}
        for i in COLUMNS_TO_DISPLAY
    ],
    data=[],
    fixed_rows={"headers": True, "data": 0},
    style_cell_conditional=[
        {"if": {"column_id": c}, "textAlign": "left"} for c in COLUMNS_TO_DISPLAY
    ],
    style_data_conditional=[
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
    ],
    style_as_list_view=True,
    style_cell={"padding": "15px"},
    style_header={
        "fontWeight": "bold",
        "font-size": "16px",
        "padding": "15px",
        "border": "3px solid black",
        "whiteSpace": "normal",
        "height": "auto",
    },
)
