import random
import string
import pandas as pd

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h4>Homework 2<h4><a href=http://127.0.0.1:5001/new-password>Password generate</a>" \
           "<p><a href=http://127.0.0.1:5001/students-info>Data average calculate</a>"


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
    return f"<h4>New password:</h4>{htmls_special_symbol(password)}"


@app.route("/students-info")
def get_average_parameters():
    df = pd.read_csv('hw.csv')
    height_avg = str(round(df[' Height(Inches)'].mean(), 2))
    weight_avg = str(round(df[' Weight(Pounds)'].mean(), 2))
    return f"<h4>Average height (Inches): {height_avg}</h4>" \
           f"<h4>Average weight (Pounds): {weight_avg}</h4>"


def htmls_special_symbol(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )


app.run(port=5001, debug=True)
