
from ast import Global
import os
from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

app = Flask(__name__)

conn =  psycopg2.connect(
    host = 'localhost',
    database = "flask_project",
    user = "postgres",
    password = "sumaiya12")

cur = conn.cursor()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app , db)
cache = Cache(app)

class Todo(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.complete = False 

@app.route('/')
def root():
    return "Hello World"
    #return redirect('/')
    #return redirect(url_for('root')) 



@app.route('/set-cache/<country>/<capital>')
def set_cache(country, capital):
    
    cache.set(country, capital)
    
    return 'Success' 

@app.route('/get-cache/<country>')
def get_cache(country):
    
    capital = cache.get(country)
    
    return capital
@app.route('/todolist')
def todolist():
    data = cache.get("all-data")

    if data is None:
        todo_list = Todo.query.all( )
        data = [] 

        for todo in todo_list:
            data.append({
                'id' : todo.id,
                'title' : todo.title,
                'complete' : todo.complete
            })
        return render_template('todo.html', todo_list = data)
    else:
        return render_template('todo.html', todo_list = data)

if __name__ == "__main__":
    app.run(debug=True)