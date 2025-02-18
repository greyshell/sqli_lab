#!/usr/bin/env python3

# author: greyshell

import os
import random
from flask import Flask, render_template
from flask import request
import sys
import pymysql
import string

templates_path = os.path.abspath(
    'template/'
)


def db_config():
    if (os.environ.get("MARIADB_USER") is None) or \
            (os.environ.get("MARIADB_PASSWORD") is None) or \
            (os.environ.get("MARIADB_DATABASE") is None) or \
            (os.environ.get("MARIADB_PORT") is None) or \
            (os.environ.get("MARIADB_HOST") is None):
        print("missing environment variable")
        sys.exit(1)


    return {
            'host': os.environ.get("MARIADB_HOST"),
            'database': os.environ.get("MARIADB_DATABASE"),
            'port': int(os.environ.get("MARIADB_PORT")),
            'user': os.environ.get("MARIADB_USER"),
            'password': os.environ.get("MARIADB_PASSWORD"),
            # 'client_flag': CLIENT.MULTI_STATEMENTS,  # enable multiple statements execution
            }


config = db_config()
app = Flask(__name__, template_folder=templates_path)


@app.route('/')
def home():
    return "App is running"


@app.route('/scenario-1', methods=['GET', 'POST'])
def vuln_scenario_1():
    if request.method == 'GET':
        return render_template("scenario-1.html")
    user = request.form.get('user')

    conn = pymysql.connect(**config)
    cur = conn.cursor()

    try:
        query = f"SELECT comment, user FROM tbl_post01 WHERE user = '{user}'"
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("scenario-1.html", results=rows)

    except pymysql.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


@app.route('/scenario-2', methods=['GET', 'POST'])
def scenario_2():
    if request.method == 'GET':
        return render_template("scenario-2.html")
    comment = request.form.get('comment')

    conn = pymysql.connect(**config)
    cur = conn.cursor()

    try:
        pin = 0  # set default value
        age = 0  # set default value
        user = 'anonymous'  # set default value
        query = f"INSERT tbl_post02 (comment, pin, age, user) VALUES ('{comment}', {pin}, {age}, '{user}')"
        # query = f"INSERT tbl_post02 (pin, comment, age, user) VALUES ({pin}, '{comment}', {age}, '{user}')"
        cur.execute(query)
        conn.commit()

        # retrieve the data
        query = "SELECT comment, pin, age, user FROM tbl_post02 WHERE user = 'anonymous'"
        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return render_template("scenario-2.html", results=rows)

    except pymysql.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


@app.route('/scenario-3', methods=['GET', 'POST'])
def tbl_post03():
    if request.method == 'GET':
        return render_template("scenario-3.html")

    comment = request.form.get('comment')

    conn = pymysql.connect(**config)
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

    except pymysql.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


@app.route('/scenario-4', methods=['GET', 'POST'])
def scenario_4():
    if request.method == 'GET':
        return render_template("scenario-4.html")
    pin = request.form.get('pin')

    conn = pymysql.connect(**config)
    cur = conn.cursor()

    try:
        comment = "anything"  # set default value
        age = 20  # set default value
        user = 'anonymous'  # set default value

        query = f"INSERT tbl_post02 (pin, comment, age, user) VALUES ({pin}, '{comment}', {age}, '{user}')"

        cur.execute(query)
        conn.commit()

        # retrieve the data
        query = "SELECT pin FROM tbl_post02 WHERE user = 'anonymous'"
        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return render_template("scenario-4.html", results=rows)

    except pymysql.Error as e:
        print(f"Error: {e}")
        cur.close()
        conn.close()


if __name__ == '__main__':
    # create the database connection
    app.run(host='0.0.0.0', port=9000, debug=True)
