""""""

from secrets import choice
from string import digits, ascii_letters
from re import fullmatch
from os import environ

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory, render_template
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main_page():
    """Explains how to use this API"""
    return send_from_directory("static", "index.html")


@app.route("/get_code/how", methods=["GET"])
def explain_create_user_code():
    """"""
    explanation = """This endpoint allows you to add your email and create a user code
for you to use when adding your data or viewing it in the future. Sending a request
will send you a follow up email with your user code that can be later recovered.
Don't forget to check your spam folder if you cannot locate it!
Structure your POST request with 'email' as a key
(could be achieved with PostMan or similar application). Alternatively,
add it yourself to the endpoint like: /get_code?email=***."""
    return render_template("explain_page.html", explanation=explanation, request="Get code")


@app.route("/recover_code/how", methods=["GET"])
def explain_recover_user_code():
    """"""
    explanation = """This endpoint allows you to get your forgotten code via email.
Don't forget to check your spam folder if you cannot locate it!
Structure your GET request with 'email' as a key
(could be achieved with PostMan or similar application). Alternatively,
add it yourself to the endpoint like: /recover_code?email=***."""
    return render_template("explain_page.html", explanation=explanation, request="Recover code")


@app.route("/get_code", methods=["POST"])
def create_user_code() -> tuple[dict, int]:
    """Creates a code for the user's POST
    request and verifies if it exists"""
    email = request.args.get("email")
    if not email:
        return {"Error": "'email' should be one of the keys for POST request!"}, 400
    if not verify_email(email):
        return {"Error": "Email is in the wrong format!"}, 400
    connection = get_db_connection()
    if check_if_email_exists(connection, email):
        connection.close()
        return {"Error": "Email is already in the database! Use /recover_code"}, 409
    code = "admin_user00"
    while(check_if_code_exists(connection, code)):
        code = generate_unique_code()
    add_user_to_db(connection, code, email)
    connection.close()
    # send_email_with_code(code, email)
    return {"Code": code}, 201


@app.route("/recover_code", methods=["GET"])
def recover_user_code() -> tuple[dict, int]:
    """"""
    email = request.args.get("email")
    if not email:
        return {"Error": "'email' should be one of the keys for this request!"}, 400
    connection = get_db_connection()
    if not check_if_email_exists(connection, email):
        connection.close()
        return {"Error": "Email does not exist! Use /get_code"}, 404
    code = find_user_code(connection, email)
    # send_email_with_code(code, email)
    return {"Code": "Email was sent with your user code associated with the email!"}, 200


def find_user_code(conn: connection, email: str) -> str:
    """"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM users WHERE email = %s""", [email])
        return cur.fetchone()["user_code"]


def add_user_to_db(conn: connection, code: str, email: str) -> None:
    """Adds user's details to the database"""
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO users(user_code, email)
    VALUES (%s, %s);""", [code, email])
        conn.commit()


def check_if_email_exists(conn: connection, email: str) -> bool:
    """Verifies if the email already exists in the database"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM users WHERE email = %s""", [email])
        data = cur.fetchall()
    return data != []


def verify_email(text: str) -> bool:
    """Returns True/False depending on if the
    full text is correctly formatted email"""
    email_regex = r"\w(?:[-\w+\.]*\w)?@\w[-\w\.]*\.[a-z]+"
    return bool(fullmatch(email_regex, text.strip()))


def get_db_connection() -> connection:
    """Returns PSQL database connection"""
    load_dotenv()
    return connect(environ["DATABASE_IP"], cursor_factory=RealDictCursor)


def generate_unique_code() -> str:
    """Generates unique 12 digit code"""
    characters = ascii_letters + digits
    return "".join(choice(characters) for _ in range(12))


def check_if_code_exists(conn: connection, potential_code: str) -> bool:
    """Verifies if the code already exists in the db"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM users WHERE user_code = %s""", [potential_code])
        data = cur.fetchall()
    return data != []


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