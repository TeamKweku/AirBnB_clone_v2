#!/usr/bin/python3
"""module starts a flask app for HBNB project"""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_state():
    """display states from the database"""
    states = storage.all("State").values()
    sorted_states = sorted(states, key=lambda x: x.name)

    return render_template("7-states_list.html", states=sorted_states)


@app.teardown_appcontext
def close_db_session(exception):
    """delete current session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
