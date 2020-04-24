import dash_core_components as dcc
import dash_html_components as html


app_header = html.Div(
    [
        html.H1("Real Estate Investment Guru", id="app-title"),
        html.H3("A tool to help guide your investment decisions", id="app-subtitle"),
    ],
    id="app-header",
)

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

model_inputs = html.Div(
            [
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
            f"By investing in this property, your discounted average ROI over the next 25 years is estimated to be between "
            f"{11.1} and {14.2}%, which represents net returns of ${670_100:,} to ${980_400:,}"
        , id="reports-text"),
    ],
    className="pretty-container",
    id="reports-section",
)