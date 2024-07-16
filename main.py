# from dash import Dash
from dash import Dash, dcc, html, Input, Output
from coinbase_lib.callback_graph import register_graph
from coinbase_lib.callback_price import register_price
from coinbase_lib.layout import layout
import dash_bootstrap_components as dbc
import os

app = Dash(__name__)
app.title = 'Crypto trading app'

app.layout = layout
register_graph(app)
register_price(app)


if __name__ == '__main__':
    app.run_server(debug=True)


