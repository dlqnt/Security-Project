from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
from werkzeug.security import check_password_hash 
from flask_wtf.csrf import CSRFProtect
#from flask_login import LoginManager
import sqlite3
import os
SECRET_KEY = "secret"

# keys for localhost. Change as appropriate.




# create and configure app
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ldh6kYiAAAAAEPBB9QMnKYpnqtzZOYk-hlikNW1'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ldh6kYiAAAAAArnDT4M2uMUObrBndRd0MOM6OLa'
# TODO: Handle login management better, maybe with flask_login?
#login = LoginManager(app)

# get an instance of the db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

# initialize db for the first time
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# perform generic query, not very secure yet
def query_db(query, one=False):
    db = get_db()
    cursor = db.execute(query)
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv

def add_user(username, first_name, last_name, password):
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = ('INSERT INTO Users (username, first_name, last_name, password) VALUES(?, ?, ?, ?)')
        cur.execute(sql, (username, first_name, last_name, password))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def get_user_by_username(username):
    """Get user details by name."""
    conn = get_db()
    cur = conn.cursor()
    try:
        sql = ("SELECT id, username FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id,username) = row
            return {
                "username": username,
                "id": id
            }
        else:
            #user does not exist
            return {
                "username": username,
                "id": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()
    
def insert_comment(p_id, u_id, comment, creation_time):
    conn = get_db()
    cur = conn.cursor() 
    try:
        sql = ('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES(?, ?, ?, ?)')
        cur.execute(sql, (p_id, u_id, comment, creation_time) )
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    finally:
        cur.close()

def insert_image(u_id, content, image, creation_time):
    conn = get_db()
    cur = conn.cursor() 
    try:
        sql = ('INSERT INTO Posts (u_id, content, image, creation_time) VALUES(?, ?, ?, ?)')
        cur.execute(sql, (u_id, content, image, creation_time) )
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    finally:
        cur.close()

def get_post(id):
    conn = get_db()
    cur = conn.cursor() 
    try:
        sql = ('SELECT * FROM Posts WHERE id= ? ;')
        cur.execute(sql, id)
        for row in cur:
            return row
        else:
            #user does not exist
            return {
                "image": None,
                "id": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def insert_friend(u_id, f_id):
    conn = get_db()
    cur = conn.cursor() 
    try:
        sql = ('INSERT INTO Friends (u_id, f_id) VALUES(?, ?);')
        cur.execute(sql, (u_id,f_id) )
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    finally:
        cur.close()

def get_hash_for_login(conn, username):
    """Get user details from id."""
    db = sqlite3.connect(app.config['DATABASE'])
    conn = db
    cur = conn.cursor()
    try:
        sql = ("SELECT password FROM Users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()
        db.close()

def valid_login(username, password):
    """Checks if username-password combination is valid."""
    # user password data typically would be stored in a database
    db = sqlite3.connect(app.config['DATABASE'])
    
    conn = db

    hash = get_hash_for_login(conn, username)
    # the generate a password hash use the line below:
    # generate_password_hash("rawPassword")
    db.close()
    
    if hash != None:
        return check_password_hash(hash, password)
    return None
# TODO: Add more specific queries to simplify code




# automatically called when application is closed, and closes db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# initialize db if it does not exist
if not os.path.exists(app.config['DATABASE']):
    init_db()

if not os.path.exists(app.config['UPLOAD_PATH']):
    os.mkdir(app.config['UPLOAD_PATH'])

from app import routes