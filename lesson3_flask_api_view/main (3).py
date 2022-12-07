import datetime
import pprint
import random
import string

import requests

from http import HTTPStatus

from flask import Flask, request, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ["Invalid request."])

    if headers:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
            headers
        )
    else:
        return jsonify(
            {
                'errors': messages
            },
            error.code,
        )


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


@app.route("/generate_password")
@use_kwargs(
    {
        "length": fields.Int(
            missing=10,
            validate=[validate.Range(min=8, max=100)]
        ),
    },
    location="query"
)
def generate_password(length):
    # length = request.args.get("length", "10")
    # max_limit = request.args.get("max_limit", "10")
    #
    # if not length.isdigit():
    #     return "ERROR: should be a digit"
    #
    # length = int(length)
    #
    # if not 8 < length < 100:
    #     return "ERROR: should be in range [8, 100]"

    return "".join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase,
        k=length
    ))


@app.route("/get_astronauts")
def get_astronauts():
    url = "http://api.open-notify.org/astros.json"
    result = requests.get(url, {})

    if result.status_code not in (HTTPStatus.OK,):
        return Response(
            "ERROR: Something went wrong",
            status=result.status_code
        )

    result = result.json()
    statistics = {}
    for entry in result.get("people", {}):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    pprint.pprint(statistics)
    return statistics


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
