import pandas as pd

from flask import Flask, request, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs, use_args

from utils import get_students, get_rates, get_symbol

app = Flask(__name__)


@app.route('/')
def hello_world():
    symbol = get_symbol('BTC')
    return '<h4>Homework 3<h4><a href=http://127.0.0.1:5001/students-generate>Students list generate</a>' \
           f'<p><a href=bitcoin-rate>{symbol} Bitcoin currency</a>'


@app.route('/students-generate')
@use_kwargs(
    {
        "count": fields.Int(
            missing=1,
            validate=[validate.Range(min=1, max=1000)]
        ),
    },
    location="query"
)
def generate_students(count):
    df = pd.DataFrame(get_students(count))
    df.to_csv('sudents.csv', index=False)
    return df.to_html(header="true", table_id="students", index=False)


@app.route('/bitcoin-rate')
@use_kwargs(
    {
        "currency": fields.Str(
            missing='USD'
        ),
        "count": fields.Int(
            missing=1,
            validate=[validate.Range(min=1, max=1000000)]
        ),
    },
    location="query"
)
def get_bitcoin_value(currency, count):
    rate = get_rates(currency)
    symbol = get_symbol(currency)
    btc_symbol = get_symbol('BTC')
    if isinstance(rate, str):
        result = rate
    else:
        result = f'BTC {count} {btc_symbol} = {currency} {count * rate} {symbol}'

    return result


app.run(port=5001, debug=True)
