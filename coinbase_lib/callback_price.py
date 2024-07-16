import requests, json
from dash import Input, Output
from datetime import datetime
import pytz

def timezone_converter(convertTime, datetimeFormater, timeZone, ):
    currentTime = datetime.strptime(convertTime, datetimeFormater)
    targetTimeZone = pytz.timezone(timeZone)

    return currentTime.astimezone(targetTimeZone).strftime("%Y-%m-%d %H:%M:%S")

def register_price(app):
    @app.callback(
        Output('price-ref', 'children'),
        Input('product-switcher', 'value')
    )
    def update_price(product_id_selection):
        denomination = product_id_selection.split('-')[1]

        url = f"https://api.exchange.coinbase.com/products/{product_id_selection}/ticker"
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers = headers)
        parse = json.loads(response.text)
        price_val = parse['price']
        timestamp = timezone_converter(parse['time'], '%Y-%m-%dT%H:%M:%S.%f%z', 'Etc/GMT-1')
        return f'{timestamp} ------ {product_id_selection} {price_val}{denomination}'

