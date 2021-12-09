from flask import Flask, redirect, url_for, render_template, request, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime 


app = Flask(__name__)

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.notesapp
notes = db.notes


app.secret_key = "bdqsrmf2"
# app.permanent_session_lifetime = timedelta(minutes=30)


#------------------------------------------------------------


@app.route("/")
def home():
    return render_template('index.html', notes=notes.find())


# Form to add new note and fill out 
@app.route('/notes/new')
def notes_new():
    return render_template('notes_new.html', title='New Note')


# Submitting the note to the database
@app.route('/notes', methods=['POST'])
def notes_submit():
    note = {
        'name': request.form.get('dname'),
        'content': request.form.get('desc'),
        'created': datetime.datetime.utcnow(),
    }
    notes.insert_one(note)
    return redirect(url_for('home'))

@app.route('/notes/<note_id>')
def notes_show(note_id):
    note = notes.find_one({'_id': ObjectId(note_id)})
    return render_template('index.html', note=note)


# Edit a note
@app.route('/notes/<notes_id>/edit')


# # Update a note
# @app.route('/notes/:id')


@app.route('/notes/:id/delete')
def delete_note():

# USER INFO --------------------------------------------------

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user


        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            # flash("Already logged in!!")
            return redirect(url_for("user"))

        return render_template('login.html')

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"), notes=notes.find())

@app.route("/logout")
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)



    