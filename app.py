#!/usr/bin/env python3

# author: greyshell

import os
import random
import string
from flask import Flask, render_template
from flask import request
import json
import constants
import mariadb

templates_path = os.path.abspath(
        './template/'
)


def db_config():
    mysql_host = os.environ.get("MYSQL_HOST", default=constants.MYSQL_HOST)
    mysql_port = os.environ.get("MYSQL_PORT", default=constants.MYSQL_PORT)
    mysql_db = os.environ.get("MYSQL_DB", default=constants.MYSQL_DB)
    try:
        import keyring
        # load db creds from linux keyring
        creds = json.loads(keyring.get_password(constants.KEYRING_SERVICE_NAME, constants.KEYRING_USERNAME))
        mysql_user = list(creds.keys())[0]
        mysql_password = list(creds.values())[0]

    except ImportError:
        # load db creds from env
        mysql_user = os.environ.get("MYSQL_USER", default=constants.MYSQL_USER)
        mysql_password = os.environ.get("MYSQL_PASSWORD", default=constants.MYSQL_PASSWORD)

    return {'user': mysql_user,
            'password': mysql_password,
            'host': mysql_host,
            'port': int(mysql_port),
            'database': mysql_db
            }


app = Flask(__name__, template_folder=templates_path)


@app.route('/')
def home():
    return "App is running"


@app.route('/scenario-1', methods=['GET', 'POST'])
def vuln_scenario_1():
    if request.method == 'GET':
        return render_template("scenario-1.html")
    user = request.form.get('user')

    config = db_config()
    conn = mariadb.connect(**config)
    cur = conn.cursor()

    try:
        query = f"SELECT comment, user FROM tbl_post01 WHERE user = '{user}'"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("scenario-1.html", results=rows)

    except mariadb.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


@app.route('/scenario-2', methods=['GET', 'POST'])
def scenario_2():
    if request.method == 'GET':
        return render_template("scenario-2.html")
    comment = request.form.get('comment')

    config = db_config()
    conn = mariadb.connect(**config)
    cur = conn.cursor()

    try:
        pin = 0  # set default value
        age = 0  # set default value
        user = 'anonymous'  # set default value
        query = f"INSERT tbl_post02 (comment, pin, age, user) VALUES ('{comment}', {pin}, {age}, '{user}')"
        cur.execute(query)
        conn.commit()

        # retrive the data
        query = "SELECT comment, pin, age, user FROM tbl_post02 WHERE user = 'anonymous'"
        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return render_template("scenario-2.html", results=rows)

    except mariadb.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


@app.route('/scenario-3', methods=['GET', 'POST'])
def tbl_post03():
    if request.method == 'GET':
        return render_template("scenario-3.html")

    comment = request.form.get('comment')

    config = db_config()
    conn = mariadb.connect(**config)
    cur = conn.cursor()

    # set default values and generate a random user
    city = 'san jose'
    age = 0
    random_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    user = 'anonymous' + '-' + random_string

    try:
        # check if the user exist
        user_input = (user,)  # pass the input in the form of a tuple
        query = "SELECT comment, city, age, user FROM tbl_post03 WHERE user = %s"
        cur.execute(query, user_input)
        rows = cur.fetchall()
        cur.close()

        if len(rows) > 0:
            return render_template("scenario-3.html", error='user already exists / had exception')

        # insert the anonymous user in tbl_post03
        cur = conn.cursor()
        query = f"INSERT tbl_post03 (comment, city, age, user) VALUES ('{comment}', '{city}', {age}, '{user}')"
        cur.execute(query)

        # Every non-holdable open cursor is implicitly closed when a transaction is terminated by COMMIT or ROLLBACK
        conn.commit()
        cur.close()  # explicit close

        # display all entries
        cur = conn.cursor()
        query = "SELECT comment, city, age, user FROM tbl_post03"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return render_template("scenario-3.html", results=rows)

    except mariadb.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


if __name__ == '__main__':
    # create the database connection
    app.run(host='0.0.0.0', port=9000, debug=True)
