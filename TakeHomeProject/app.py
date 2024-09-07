"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, redirect, render_template, request
import mysql.connector

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

mydb=mysql.connector.connect(host="localhost", user="YOUR USER", password="YOUR PASSWORD", database="mydatabase")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS loginData (username VARCHAR(255), password VARCHAR(255))")

mycursor.execute("SELECT * FROM loginData")
mycursor.fetchall()

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        mycursor.execute("SELECT password FROM loginData WHERE username = %s", (username,))
        user = mycursor.fetchone()

        if user:
            pass_match = user[0]
            if password == pass_match:
                return render_template('index.html')
            else:
                message = "Username or password is incorrect."
                return render_template('login.html',message=message)
                       
        else:
            message = "Username does not exist."
            return render_template('login.html', message=message)

    return render_template('login.html')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm-password")

        if password != confirm:
            message = "Passwords do not match"
            return render_template('register.html', message=message)
        
        mycursor.execute("SELECT * FROM loginData WHERE username = %s", (username,))
        existing_user = mycursor.fetchone()

        if existing_user:
            message = "Username is already taken"
            return render_template('register.html', message=message)
            
        # If everything is fine, insert the new user into the database
        mycursor.execute("INSERT INTO loginData (username, password) VALUES (%s, %s)", (username, password))
        mydb.commit()

        return render_template("index.html")

    return render_template('register.html')


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
