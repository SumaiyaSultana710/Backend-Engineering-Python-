
from flask import Flask, render_template, redirect, url_for, request, make_response

app = Flask(__name__)
count = 1

todo_list = []

class Todo:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.complete = False

@app.route('/')
def root():
    return "Hello World"
    #return redirect('/')
    #return redirect(url_for('root')) 

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

@app.route('/todolist')
def todolist():
    return render_template('todo.html', todo_list = todo_list)


@app.route('/addtodo', methods = ['POST'])
def add_todo():
    global count
    title = request.form['title']
    todo = Todo(count, title)
    count += 1
    
    todo_list.append(todo)

    return redirect(url_for('todolist')) 

@app.route('/updatetodo/<complete>/<int:id>')
def update_todo(complete,id):
    for todo in todo_list:
        if todo.id == id:
            if complete == "complete":
                todo.complete = True
                break
            elif complete == "incomplete":
                todo.complete = False
                break
    return redirect(url_for('todolist')) 

@app.route('/deletetodo/<int:id>')
def delete_todo(id):
    for todo in todo_list:
        if todo.id == id:
            todo_list.remove(todo)
    return redirect(url_for('todolist')) 


if __name__ == "__main__":
    app.run(debug=True)