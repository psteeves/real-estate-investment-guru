import dash_html_components as html

import dash

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Real Estate Investment Guru"),
        html.H5("A tool to help guide your investment decisions")
    ]
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
