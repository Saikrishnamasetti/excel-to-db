from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'

# db = SQLAlchemy(app)


# class Persons(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     mobileNo = db.Column(db.Integer)
#     emailID = db.Column(db.String(100))
#     registrationNo = db.Column(db.Integer)
#     registrationCouncil = db.Column(db.String(10))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name == 'admin' and password == 'admin':
            return redirect('/upload')
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.form['file']
        df = pd.read_excel(file)
        engine = create_engine('sqlite:///person.db', echo=True)
        sqliteConnection = engine.connect()
        df.to_sql('persons', sqliteConnection, if_exists='append')
        sqliteConnection.close()
        return redirect('/data')
    return render_template('upload.html')


@app.route('/data')
def data():
    conn = sqlite3.connect('person.db')
    c = conn.cursor()
    c.execute('SELECt * FROM persons')
    data = c.fetchall()
    return render_template('data.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
