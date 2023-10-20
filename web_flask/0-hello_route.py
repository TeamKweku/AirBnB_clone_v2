#!/usr/bin/python3
"""flask script that prints a route when using curl"""


from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """method for the hello route"""
    return "Hello HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
