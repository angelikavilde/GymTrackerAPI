""""""

from flask import Flask, jsonify, request, send_from_directory


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    """Explains how to use this API"""
    return send_from_directory("static", "index.html")


@app.route("/add", methods=["POST"])
def add_workout():
    """Logs in a new workout"""
    workout_data = request.json
    return jsonify(workout_data), 201


@app.route("/add/how", methods=["GET"])
def explain_add_workout():
    pass


if __name__=="__main__":
    app.run(port = 5040, debug = True, host = "0.0.0.0")