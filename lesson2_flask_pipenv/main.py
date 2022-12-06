import datetime

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    # view
    return "<p>Hello, World!!!!</p>"


@app.route("/mykhailo")
def hello_mykhailo():
    return "<p>Hello, Mykhailo!!!!</p>"


@app.route("/now")
def get_time():
    return f"current time: {datetime.datetime.now()}"


# rote
def generate_password():
    """
    1. ascii_lowercase
    2. ascii_uppercase
    3. int
    4. special symbols
    5. random length [10-20]
    """


# rote
def get_average_parameters():
    """
    1. calculate average weight
    2. calculate average height
    3. use csv lib
    *4. use pandas lib
    """
    pass


app.run(port=5001, debug=True)

# http://127.0.0.1:5001/profile?a=1
# http://127.0.0.1:5001/about/
