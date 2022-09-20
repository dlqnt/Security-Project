"""
Flask: Login
"""

from setup_db import *
from flask import Flask, request, redirect, url_for, flash, session, g, abort
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'some_secret'

def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()

def valid_login(username, password):
    """Checks if username-password combination is valid."""
    # user password data typically would be stored in a database
    conn = get_db()

    hash = get_hash_for_login(conn, username)
    # the generate a password hash use the line below:
    # generate_password_hash("rawPassword")
    if hash != None:
        return check_password_hash(hash, password)
    return False


# The first three routes do not fit into a rest API. 

@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    if not valid_login(data.get("username", ""), data.get("password", "")):
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn,data["username"])
    #user["contacts"] = get_user_contacts(conn, user["userid"])
    #print(user)
    session["userid"] = user["userid"]
    return user

@app.route("/logout")
def logout():
    session.pop("userid")
    return "OK"

# Here comes the rest API for contacts.
@app.route("/user", methods=["GET"])
def get_user():
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    conn = get_db()
    user = get_user_by_id(conn,userid)
    return json.dumps(user)



@app.route("/contacts", methods=["GET"])
def get_contacts():
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    conn = get_db()
    
    contacts = get_user_contacts(conn, userid)
    return json.dumps(contacts)

@app.route("/contacts", methods=["POST"])
def add_contact():
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    
    newcontact = request.get_json()
    if len(newcontact.get("name", "")) == 0:
        abort(400)

    conn = get_db()
    newid = insert_contact(conn, newcontact["name"], 
                            newcontact.get("email", None),
                            newcontact.get("phone", None), 
                            userid)

    return str(newid)

@app.route("/contacts/<contactid>", methods=["PUT"])
def set_contact(contactid):
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    
    contact = request.get_json()
    if len(contact.get("name", "")) == 0 or contact.get("id", "-1") != contactid:
        abort(400)

    conn = get_db()
    affected = update_contact(conn, contact,
                            userid)

    if affected == 0:
        abort(400)

    return "OK"

@app.route("/contacts/<contactid>", methods=["DELETE"])
def del_contact(contactid):
    userid = session.get("userid", None)
    if userid == None:
        abort(404)
    
    conn = get_db()
    affected = delete_contact(conn, contactid,
                            userid)

    if affected == 0:
        abort(400)

    return "OK"
    



if __name__ == "__main__":
    app.run()