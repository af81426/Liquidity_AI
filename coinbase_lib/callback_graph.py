
import requests, json
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output
from ta import momentum
from ta.trend import MACD
from plotly.subplots import make_subplots

from coinbase_lib.get_candlesticks import get_candlestick_data


def create_dataframe(df):
    df = df.sort_values(by='timestamp')
    df['diff'] = df['price_close'] - df['price_open']
    df.loc[df['diff'] >= 0, 'color'] = 'green'
    df.loc[df['diff'] < 0, 'color'] = 'red'

    df['rsi'] = momentum.rsi(df['price_close'], window=14, fillna=False)
    df['MA20'] = df['price_close'].rolling(window=20).mean()
    df['MA7'] = df['price_close'].rolling(window=7).mean()

    df['1D'] = (df.price_close - df.price_close.shift(1))

    df = df.assign(
        R_spread=(df.price_high - df.price_low) / (0.5 * (df.price_high + df.price_low) ),
        Amihud=abs(df['1D']) / df.volume,
        Roll=df['1D'].rolling(window=20).apply(lambda x: pd.Series(x).autocorr(), raw=False)
    )

    return df

def render_price(df):
    max_volume = df["volume"].max()

    macd = MACD(close=df["price_close"], window_slow=26, window_fast=12, window_sign=9)

    fig1 = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=False,
        horizontal_spacing=0.05,
        row_heights=[0.8, 0.4, 0.3, 0.3],
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}],
        ],
    )
    fig1.add_trace(
        go.Candlestick(
            x=df["timestamp"],
            open=df["price_open"],
            high=df["price_high"],
            low=df["price_low"],
            close=df["price_close"],
            name="Price",
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["MA20"],
            opacity=0.7,
            line=dict(color="blue", width=2),
            name="MA 20",
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["MA7"],
            opacity=0.7,
            line=dict(color="orange", width=2),
            name="MA 7",
        )
    )
    fig1.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["volume"],
            name="Volume",
            marker={"color": df["color"]},
        ),
        # secondary_y=True,
        row=2, col=1
    )
    fig1.add_trace(go.Bar(x=df["timestamp"], y=macd.macd_diff()), row=3, col=1)
    fig1.add_trace(
        go.Scatter(x=df["timestamp"], y=macd.macd(), line=dict(color="black", width=2)),
        row=3,
        col=1,
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"], y=macd.macd_signal(), line=dict(color="red", width=1)
        ),
        row=3,
        col=1,
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["rsi"],
            mode="lines",
            line=dict(color="purple", width=1),
        ),
        row=4,
        col=1,
    )

    fig1.update_layout(height=1200, showlegend=False, xaxis_rangeslider_visible=False)

    fig1.update_yaxes(title_text="<b>Price</b>", row=1, col=1)
    fig1.update_yaxes(
        title_text="<b>Volume</b>",
        range=[0, max_volume * 1.2],
        row=2,
        col=1,
        # secondary_y=True,
    )
    fig1.update_yaxes(title_text="<b>MACD</b>", showgrid=False, row=3, col=1)
    fig1.update_yaxes(title_text="<b>RSI</b>", row=4, col=1)
    return fig1

def render_liquidity(df):

    fig1 = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=False,
        horizontal_spacing=0.05,
        row_heights=[0.4, 0.4, 0.4, 0.4],
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": True}],
        ],
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["R_spread"],
            opacity=0.7,
            line=dict(color="red", width=2),
            name="R Spread",
        ), row=1, col=1
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price_close"],
            opacity=0.5,
            line=dict(color="blue", width=2),
            # marker={"color": df["color"]},
            name="Close Price",
        ),
        secondary_y=True,
        row=1, col=1
    )

    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["Amihud"],
            opacity=0.7,
            line=dict(color="red", width=2),
            name="Amihud",
        ), row=2, col=1
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price_close"],
            opacity=0.5,
            line=dict(color="blue", width=2),
            # marker={"color": df["color"]},
            name="Close Price",
        ),
        secondary_y=True,
        row=2, col=1
    )

    fig1.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["volume"],
            name="Volume",
            marker={"color": df["color"]},
        ),
        # secondary_y=True,
        row=3, col=1
    )

    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["Roll"],
            opacity=0.7,
            line=dict(color="red", width=2),
            name="Roll",
        ), row=4, col=1
    )
    fig1.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["price_close"],
            opacity=0.5,
            line=dict(color="blue", width=2),
            # marker={"color": df["color"]},
            name="Close Price",
        ),
        secondary_y=True,
        row=4, col=1
    )
    fig1.update_layout(height=1200, showlegend=False, xaxis_rangeslider_visible=False)
    fig1.update_yaxes(title_text="<b>R Spread</b>", row=1, col=1)
    fig1.update_yaxes(title_text="<b>Close Price</b>", row=1, col=1, secondary_y=True,)
    fig1.update_yaxes(title_text="<b>Amihud</b>", row=2, col=1)
    fig1.update_yaxes(title_text="<b>Close Price</b>", row=2, col=1, secondary_y=True,)
    fig1.update_yaxes(title_text="<b>Volume</b>", row=3, col=1)
    fig1.update_yaxes(title_text="<b>Roll</b>", row=4, col=1)
    fig1.update_yaxes(title_text="<b>Price</b>", row=4, col=1, secondary_y=True,)

    return fig1

def register_graph(app):

    @app.callback(
        Output("product-chart", "figure"),
        Input("product-switcher", "value"),
        Input("gran-switcher", "value"),
        Input("content-switcher", "value")
    )
    def update_output(product_id_selection, granularity_selection, content_selection):
        raw = get_candlestick_data(product_id_selection, granularity_selection)
        df = create_dataframe(raw)
        df.to_csv(r"C:\Users\Anqi.Fu\dev\AI_liquidity\data.csv")

        if content_selection == 'Price':
            return render_price(df)
        else:
            return render_liquidity(df)
