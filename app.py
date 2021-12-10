from flask import Flask, redirect, url_for, render_template, request, session, flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import os
import datetime


app = Flask(__name__)

bcrypt = Bcrypt(app)

host = os.environ.get('DB_URL')
client = MongoClient(host=host)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

# mongo = PyMongo(app)
db = client.notesapp
notes = db.notes

users = db.user

app.secret_key = "bdqsrmf2"
# app.permanent_session_lifetime = timedelta(minutes=30)


#------------------------------------------------------------

''' SHOW ALL NOTES ------------------------------------------------- '''
@app.route("/")
def home():
    return render_template('index.html')



''' CREATE NEW NOTE ------------------------------------------------- '''
@app.route("/notes/new", methods=['GET'])
def notes_new():
    _id = session['_id']
    return render_template('notes_new.html', title='New Note', _id=_id)


''' SUBMIT A NEW NOTE ------------------------------------------------- '''
@app.route("/notes", methods=['POST'])
def notes_submit():
    _id = session['_id']
    note = {
        'name': request.form.get('dname'),
        'content': request.form.get('desc'),
        'created': datetime.datetime.utcnow(),
        'user_id': _id
    }
    notes.insert_one(note)
    return redirect(url_for('home'))

''' EDIT A NOTE  '''
@app.route("/notes/<notes_id>/edit")
def notes_edit(notes_id):
    note = notes.find_one({'_id': ObjectId(notes_id)})
    return render_template('notes_edit.html', note=note, title='Edit Playlist')


''' SUBMIT THE EDITED NOTE ------------------------------------------------- '''
@app.route("/notes/<notes_id>", methods=['POST'])
def notes_update(notes_id):
    updated_note = {
        'name': request.form.get('title'),
        'content': request.form.get('description'),
        'created': datetime.datetime.utcnow(),
    }

    notes.update_one(
        {'_id': ObjectId(notes_id)},
        {'$set': updated_note})
    return redirect(url_for('user', notes_id=notes_id, title='Edit Playlist'))

''' DELETE A NOTE ------------------------------------------------- '''

@app.route("/notes/<notes_id>/delete", methods=['POST'])
def notes_delete(notes_id):
    """Delete one playlist."""
    notes.delete_one({'_id': ObjectId(notes_id)})
    return redirect(url_for('user'))




# USER -----------------------------------------------------------------------------


'''HELPER FUNCTIONS ---------------------------------------------------------------------- '''

def logged_in():
    return session.get('username') and session.get('password')

def current_user():
    found_user = users.find_one ({
        'username':session.get('username'),
        'password':session.get('password')
    })
    return found_user
    


@app.route("/user")
def user():
    if logged_in:
        user = current_user()
        _id = session['_id']

        return render_template("user.html", _id=_id, user=user, notes=notes.find({'user_id': _id}).sort([['_id', -1]]))
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"), notes=notes.find())
        
'''LOGIN AND LOGOUT ROUTES -----------------------------------------'''


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        email = request.form['logname']
        password = request.form['logpass']
        user = users.find_one({'username': email})
        if user:
            if bcrypt.check_password_hash(user['password'], password):
                session['email'] = user['username']
                session['_id'] = str(user['_id'])
                return redirect(url_for('user'))
            else:
                flash("Incorrect username/password")
            pass 
        else:
            flash("Incorrect username/password 2")
            return render_template('login.html')
    else:
        if "email" in session:
            # flash("Already logged in!!")
            return redirect(url_for("user"))
        else:
            return render_template('login.html')


@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("email", None)
    return redirect(url_for("login"))


''' REGISTER A USER ---------------------------------------- '''


@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup_form():
    username = request.form.get("usern")
    password = request.form.get("passw")
    password_hash = bcrypt.generate_password_hash(password)
    name = request.form.get("sname")

    found_user = users.find_one({'username':username})
    if found_user:
        flash("User already exists")
        return redirect(url_for('signup'))
    
    user = {
        'username':username,
        'password':password_hash,
        'name':name,
        'created':datetime.datetime.utcnow()
    }

    users.insert_one(user)

    # session["username"] = user['username']
    # session["password"] = user['password']

    return redirect(url_for("user"))



if __name__ == "__main__":
    app.run(debug=True)



    