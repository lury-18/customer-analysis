import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import sqlalchemy

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=([dbc.themes.BOOTSTRAP]))


CONTENT_STYLE = {
    "margin-left": "0.5rem",
    "margin-right": "0.5rem",
    "padding": "2rem 1rem",
    'display': 'inline-block'
}

# dummy components for layout

card_ongoing = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title"),
            html.H6("Card subtitle", className="card-subtitle"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "18rem"},
)

card_delayed = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Title", className="card-title"),
            html.H6("Card subtitle", className="card-subtitle"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", href="https://google.com"),
        ]
    ),
    style={"width": "18rem"},
)


df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
dummy_pie_chart = px.pie(df, values='pop', names='country', title='Population of European continent')

# app.layout = html.Div([
#     html.Div(style= {"margin": "1rem"}, children=[html.H1("Delivery Tracking System")]),
    
#     html.Div([
#         html.Div(children=[card_ongoing, card_delayed], className="three columns"),
        
#         html.Div(children=[dcc.Graph(id='pie', figure=dummy_pie_chart)], className="three columns"),
        
#         html.Div(children=[card_ongoing], className="six columns")
#         ], className = 'row')
#     ])

app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(style= {"margin": "1rem"}, children=[html.H1("Delivery Tracking System")]))),
        dbc.Row(
            [
                dbc.Col(html.Div([card_ongoing, card_delayed]), width=4),
                dbc.Col(children=[dcc.Graph(id='pie', figure=dummy_pie_chart)]),
                dbc.Col(html.Div(children=[card_ongoing]), width=4),
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)