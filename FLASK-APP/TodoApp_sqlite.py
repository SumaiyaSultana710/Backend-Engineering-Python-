
from ast import Global
import os
from flask import Flask, render_template, redirect, url_for, request, make_response
import psycopg2

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os .environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir , 'app.db')

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



if __name__ == "__main__":
    app.run(debug=True)