import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import sqlalchemy

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1("Recommendation System")
])


if __name__ == '__main__':
    app.run_server(debug=True)