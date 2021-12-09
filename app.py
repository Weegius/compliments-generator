from flask import Flask, redirect, url_for, render_template, request, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import os
import datetime 


app = Flask(__name__)

bcrypt = Bcrypt(app)

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.notesapp
notes = db.notes
users = db.user
records = db.register


app.secret_key = "bdqsrmf2"
# app.permanent_session_lifetime = timedelta(minutes=30)


#------------------------------------------------------------

''' SHOW ALL NOTES ------------------------------------------------- '''
@app.route("/")
def home():
    return render_template('index.html', notes=notes.find())


''' CREATE NEW NOTE ------------------------------------------------- '''
@app.route("/notes/new")
def notes_new():
    return render_template('notes_new.html', title='New Note')


''' SUBMIT A NEW NOTE ------------------------------------------------- '''
@app.route("/notes", methods=['POST'])
def notes_submit():
    note = {
        'name': request.form.get('dname'),
        'content': request.form.get('desc'),
        'created': datetime.datetime.utcnow(),
    }
    notes.insert_one(note)
    return redirect(url_for('home'))

''' SHOW A NOTE ------------------------------------------------- '''
# @app.route('/playlists/<playlist_id>')  
# def playlists_show(playlist_id):
#     """Show a single playlist."""
#     playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
#     playlist_comments = comments.find({'playlist_id': playlist_id})
#     return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

''' EDIT A NOTE  '''
@app.route("/notes/<notes_id>/edit")
def notes_edit(notes_id):
    note = notes.find_one({'_id': ObjectId(notes_id)})
    return render_template('notes_edit.html', note=note, title='Edit Playlist')


''' SUBMIT THE EDITED NOTE ------------------------------------------------- '''
@app.route("/notes/<note_id>", methods=['POST'])
def notes_update(notes_id):
    updated_note = {
        'name': request.form.get('dname'),
        'content': request.form.get('desc'),
        'created': datetime.datetime.utcnow(),
    }

    notes.update_one(
        {'_id': ObjectId(notes_id)},
        {'$set': updated_note})
    return redirect(url_for('user.html', notes_id=notes_id, title='Edit Playlist'))

''' DELETE A NOTE ------------------------------------------------- '''

@app.route("/notes/<notes_id>/delete", methods=['POST'])
def notes_delete(notes_id):
    notes.delete_one({'_id': ObjectId(notes_id)})
    return redirect(url_for('user'))






    

# USER INFO -----------------------------------------------------------------------------

def logged_in():
    return session.get('username') and session.get('password')
def current_user():
    found_user = users.find_one({
        'username':session.get('username'),
        'password':session.get('password')
    })
    return found_user



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
        return render_template("user.html", user=user, notes=notes.find())
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



    