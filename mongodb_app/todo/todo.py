from flask import Blueprint, Flask, render_template, request, url_for, redirect, session
import pymongo
from bson import ObjectId

# default mongodb configuration - Remote database
client = pymongo.MongoClient(
    "mongodb+srv://cafe:yYCEj4BSsl0zgifW@cluster0.lz9tjnm.mongodb.net/?retryWrites=true&w=majority")
# database:
db = client.flask_db
# collections:
todos = db.todos
records = db.register

todo_bp = Blueprint('todo_bp', __name__, template_folder='templates', static_folder='static')


@app.route('/todolist', methods=('GET', 'POST'))
def todolist():
    """
    Display the todo list and allow adding new items.
    If the request method is POST, add a new item to the list.
    * content: The content of the new item.
    * degree: The degree of the new item.
    :return: The todo list page.
    """
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('todolist'))

    all_todos = todos.find()
    return render_template('/todolist', todos=all_todos)


@app.post('/<id>/delete')
def delete(id):
    """
    Delete an item from the list.

    * id: The id of the item to delete.

    :return: Redirect to the index page.
    """
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))
    

