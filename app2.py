import os
import psycopg2
from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import date, timedelta

app = Flask(__name__)


def db_connection():  # connecting to database: bdr_test
    #os.environ['DB_USERNAME'] = 'postgres'
    #os.environ['DB_PASSWORD'] = '123'

    connection = psycopg2.connect(host='localhost',
                                  port=50001,
                                  database='test',
                                  user='postgres',
                                  password='postgrespw')
    return connection


def search_by_username(username):
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT* FROM users WHERE username = %s;", (username,))
    attributes = cursor.fetchall()

    cursor.close()
    connection.close()

    if len(attributes) != 0:
        return attributes[0]
    else:
        return []


@app.route('/')
def home():

    return "Hello"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form['username']
        attributes = search_by_username(username)
        if len(attributes) == 0:  # username not registered in the database
            error = "username or password is wrong"
        elif request.form['password'] != attributes[2]:   # given password is not match in the database
            error = "username or password is wrong"
        elif attributes[4] + timedelta(days=30) < date.today():  # subscription time is over
            return render_template('login.html', error=error), 403
        else:
            return redirect(url_for('home'))

    return render_template('login.html', error=error), 404


@app.route('/signup', methods=['POST'])
def sign_up():
    connection = db_connection()
    cursor = connection.cursor()
    userAttributes = request.get_json()

    username = userAttributes['username']
    password = userAttributes['password']
    fullname = userAttributes['real_name']

    if len(search_by_username(username)) != 0:
        return jsonify({"success": False, "response": "username is already taken."})
    else:
        cursor.execute('INSERT INTO users (username, password, real_name)'
                       'VALUES (%s, %s, %s)',
                       (username,
                        password,
                        fullname)
                       )
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"success": True, "response": "User added"})


@app.route('/update', methods=['PATCH'])
def add_subscription_time():

    username = request.get_json()['username']

    if len(search_by_username(username)) == 0:
        return jsonify({"success": False, "response": "user not found.", "Status Code": 404}), 404
    else:
        today = date.today()
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET subscription_start = %s WHERE username = %s;", (today, username))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "response": "subscription time renewed!", "Status Code": 200}), 200


@app.route('/delete', methods=['DELETE'])
def delete_user():

    username = request.get_json()['username']

    if len(search_by_username(username)) == 0:
        return jsonify({"success": False, "response": "user not found.", "Status Code": 404}), 404
    else:
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s;", (username,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "response": "user successfully deleted!", "Status Code": 200}), 200


if __name__ == '__main__':

    # app.run()
    app.run(debug=True)
