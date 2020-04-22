import dash_core_components as dcc
import dash_html_components as html

import dash

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Real Estate Investment Guru"),
                html.H4("A tool to help guide your investment decisions"),
            ],
            id="app-header",
        ),
        html.Div(
            [
                html.P("What is your downpayment budget?", className="control-label",),
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
                    tooltip={'visible': True},
                    className="dcc-control",
                ),
            ],
            className="pretty-container",
        ),
    ]
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_props_check=False)
