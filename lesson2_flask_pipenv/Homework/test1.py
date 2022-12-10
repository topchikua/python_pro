import datetime
import random
import string
import pandas as pd

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    # view
    return "<p>Hello, World!!!!</p>"


@app.route("/new-password")
def generate_password():
    symbol_types = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    temp = symbol_types.copy()
    symbol_len = random.randint(10, 19)
    password = ''
    for i in range(symbol_len):
        if i <= 3:
            symbol = random.choices(temp)
            password += ''.join(random.choices(symbol[0]))
            temp.pop(temp.index(symbol[0]))
        elif i >= 4:
            symbol = random.choices(symbol_types)
            password += ''.join(random.choices(symbol[0]))
    return f"<h3>New password:</h3>" + password


@app.route("/students-info")
def get_average_parameters():
    pd.options.display.max_rows = 10

    df = pd.read_csv('hw.csv')

    print(pd.options.display.max_rows)
    print(df)

    return f"current time: {datetime.datetime.now()}"


app.run(port=5001, debug=True)
