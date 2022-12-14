
from ast import Global
import os
from flask import Flask, render_template, redirect, url_for, request, make_response
import psycopg2
# import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
#count = 1


conn =  psycopg2.connect(
    host = 'localhost',
    database = "flask_project",
    user = "postgres",
    password = "sumaiya12")

# using mysql
# conn =  mysql.connector.connect(
#     host = 'localhost',
#     database = "flask_project",
#     user = "root",
#     password = "")

cur = conn.cursor()

# todo_list = []


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os .environ.get('DATABASE_URL') or 'postgresql://postgres:sumaiya12@localhost:5432/flask_project'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app , db)

class Todo(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.complete = False 

# class Todo:
#     def __init__(self, id, title):
#         self.id = id
#         self.title = title
#         self.complete = False

@app.route('/')
def root():
    return "Hello World"
    #return redirect('/')
    #return redirect(url_for('root')) 

@app.route('/todolist')
def todolist():
    todo_list = Todo.query.all( )
    return render_template('todo.html', todo_list = todo_list)

@app.route('/addtodo', methods = ['POST'])
def add_todo():
    
    title = request.form.get('title')
    new_todo = Todo(title = title)
    db.session.add(new_todo)
    db.session.commit()
    
    return redirect(url_for('todolist')) 

@app.route('/updatetodo/<complete>/<int:todo_id>')
def update_todo(complete,todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('todolist')) 


@app.route('/deletetodo/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todolist')) 


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
@app.route('/home/<argument>')
def home(argument = None):
    return f"My name is {argument}"

@app.route('/dashboard')
@app.route('/dashboard/<argument>')
def dashboard(argument = None):
    return render_template('dashboard.html', name = argument)

@app.route('/dict')
def dict():
    dict = { 
        "Bangladesh" : "Dhaka",  
        "India" : "Delhi" }
    # return dict
    return make_response(dict), 202

# @app.route('/todolist')
# def todolist():
#     return render_template('todo.html', todo_list = todo_list)

# @app.route('/addtodo', methods = ['POST'])
# def add_todo():
#     global count
#     title = request.form['title']
#     todo = Todo(count, title)
#     count += 1
    
#     todo_list.append(todo)

#     return redirect(url_for('todolist')) 

# @app.route('/updatetodo/<complete>/<int:id>')
# def update_todo(complete,id):
#     for todo in todo_list:
#         if todo.id == id:
#             if complete == "complete":
#                 todo.complete = True
#                 break
#             elif complete == "incomplete":
#                 todo.complete = False
#                 break
#     return redirect(url_for('todolist')) 

# @app.route('/deletetodo/<int:id>')
# def delete_todo(id):
#     for todo in todo_list:
#         if todo.id == id:
#             todo_list.remove(todo)
#     return redirect(url_for('todolist')) 



#### use of postgres cursor without ORM, direct query 

@app.route('/get-db')
def get_db():
    cur.execute('SELECT version()')
    #display postgres db version
    db_version = cur.fetchone()
    print(db_version)

    #close the communication with postgres
    cur.close()
    return 'True'


if __name__ == "__main__":
    app.run(debug=True)