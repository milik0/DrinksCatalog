# import required packages
import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, url_for, redirect, session
import bcrypt

# initialize Flask app and set a secret key
app = Flask(__name__)
app.secret_key = "testing"

# define MongoDB client and collections
client = pymongo.MongoClient(
    "mongodb+srv://milik0:ShgoX7c0b3YXAxhd@cluster0.qmvimn4.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
todos = db.todos
records = db.register

# define route for index page
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template('index.html')

# define route for registration page
@app.route("/register/", methods=['post', 'get'])
def register():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))

    # handle form submission
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # check if user already exists
        user_found = records.find_one({"name": user})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)

        # check if email already exists
        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)

        # check if passwords match
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)

        # hash the password and insert user data into database
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)

    # display registration page
    return render_template('register.html')

# define route for about page
@app.route('/about/')
def about():
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))
    return render_template('about.html')

# define route for login page
@app.route("/login/", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if the email exists in the database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            # check if the entered password matches the hashed password in the database
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                # if password does not match, redirect back to login page with error message
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            # if email is not found in the database, redirect back to login page with error message
            message = 'Email not found'
            return render_template('login.html', message=message)
    # if request is not POST, display the login page
    return render_template('login.html', message=message)

# define route for logged_in page
@app.route('/logged_in/')
def logged_in():
    # Check if the user is logged in
    if "email" in session:
        # Retrieve the user's email from the session
        email = session["email"]
        # Render the logged_in.html template with the user's email
        return render_template('logged_in.html', email=email)
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for("login"))


# route for logging out
@app.route("/logout/", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("sign_out.html")
    else:
        return render_template('index.html')


# define route for todolist page
@app.route('/todolist/', methods=('GET', 'POST'))
def todolist():
    # Check if the user is logged in
    message = ''
    if "email" not in session:
        return redirect(url_for("login"))

    # handle form submission
    if request.method == 'POST': 
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('todolist')) # redirect to todolist page 

    # display todolist page
    all_todos = todos.find()
    return render_template('todolist.html', todos=all_todos)

# define route for delete
@app.post('/<id>/delete')
def delete(id):
    # delete todo from database
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('todolist'))

# define route for modify
@app.post('/<id>/modify')
def modify(id):
    # modify todo from database
    elm = todos.find({"_id":ObjectId(id)})[0]
    myquery = { "content":  elm['content']}
    newvalues = { "$set": { "content": request.form['content'] , 'degree': request.form['degree']} }
    todos.update_one(myquery, newvalues)
    return redirect(url_for('todolist'))

if __name__ == '__main__':
    app.run()
