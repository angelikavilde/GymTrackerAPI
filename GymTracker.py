""""""

from secrets import choice
from string import digits, ascii_letters
from os import environ

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    """Explains how to use this API"""
    return send_from_directory("static", "index.html")


@app.route("/get_code", methods=["GET"])
def get_user_code() -> str:
    """Creates a code for the user's POST
    request and verifies if it exists"""
    code = "admin_user00"
    connection = get_db_connection()
    while(check_if_code_exists(connection, code)):
        code = generate_unique_code()
        print(code)
    return str(code)


def get_db_connection() -> connection:
    """Returns PSQL database connection"""
    load_dotenv()
    return connect(environ["DATABASE_IP"], cursor_factory=RealDictCursor)


def generate_unique_code() -> str:
    """Generates unique 12 digit code"""
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(12))


def check_if_code_exists(conn: connection, code: str) -> bool:
    """Verifies if the code already exists in the db"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM users WHERE user_code = %s""", [code])
        data = cur.fetchall()
    return data is not None


@app.route("/add", methods=["POST"])
def add_workout():
    """Logs in a new workout"""
    # workout_data = request.json
    # return jsonify(workout_data), 201
    pass


@app.route("/add/how", methods=["GET"])
def explain_add_workout():
    pass


if __name__=="__main__":
    app.run(port = 5040, debug = True, host = "0.0.0.0")