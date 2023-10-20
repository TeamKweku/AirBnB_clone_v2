#!/usr/bin/python3
"""flask script that prints a route when using curl"""


from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """method for the hello route"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """method for the hbnb route"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """method for the hbnb route"""
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
