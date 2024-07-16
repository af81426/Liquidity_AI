from dash import html, dcc

layout = html.Div(
    children=[
        html.H1(children='Coinbase'),
        html.Div(id='price-ref', style={'padding-top': 10, 'font-size': '22px'}),
        html.Div(
            [
                dcc.Dropdown(
                    [
                        'BTC-GBP',
                        'BTC-USD',
                        # 'CRV-USD',
                        # 'SOL-USD',
                        # 'CBETH-USD',
                        # 'CBETH-ETH',
                    ],
                    'BTC-GBP',
                    id='product-switcher',
                    clearable=False,
                    style={'width': '150px'},
                ),
                dcc.Dropdown(
                    # options={
                    #     '60': 'M1',
                    #     '300': 'M5',
                    #     '900': 'M15',
                    #     '3600': 'H1',
                    #     '21600': 'H6',
                    #     '86400': 'D1',
                    # },
                    [
                        'M1',
                        'M5',
                        'M15',
                        'H1',
                        'H6',
                        'D1',
                    ],
                    'D1',
                    id='gran-switcher',
                    clearable=False,
                    style={'width': '150px'},
                ),
                dcc.Dropdown(
                    [
                        'Price',
                        'Liquidity'
                    ],
                    'Price',
                    id='content-switcher',
                    clearable=False,
                    style={'width': '150px'},
                )
            ]
        ),
        dcc.Graph(id='product-chart', style={'width': '90%'})
    ]
)

