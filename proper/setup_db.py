import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def create_user_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE users ("
               "userid INTEGER, "
               "username VARCHAR(20) NOT NULL, "
               "passwordhash VARCHAR(120) NOT NULL, "
               "PRIMARY KEY(userid) "
               "UNIQUE(username))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()

def create_contact_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE contacts ("
               "contactid INTEGER, "
               "userid INTEGER, "
               "name TEXT NOT NULL, "
               "phone TEXT, "
               "email TEXT, "
               "PRIMARY KEY(contactid) "
               "FOREIGN KEY (userid) REFERENCES users (userid))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()

def add_user(conn, username, hash):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users (username, passwordhash) VALUES (?,?)")
        cur.execute(sql, (username, hash))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def insert_contact(conn, name, email,phone, userid):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO contacts (userid,name, email, phone) VALUES (?,?,?,?)")
        cur.execute(sql, (userid, name, email, phone))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("contact {} added with id {}.".format(name, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def update_contact(conn, contact, userid):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("UPDATE contacts SET "
                "name=?, email=?, phone=? "
                "WHERE contactid = ? AND userid = ?")
        cur.execute(sql, (contact["name"], 
                        contact.get("email",None),
                        contact.get("phone",None), 
                        contact.get("id",None), 
                        userid))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Updates {} contacts.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()

def delete_contact(conn, contactid, userid):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM contacts "
                "WHERE contactid = ? AND userid = ?")
        cur.execute(sql, (contactid, 
                        userid))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Removed {} contacts.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()

def get_user_contacts(conn, userid):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT contactid, name, phone, email FROM contacts WHERE userid = ?")
        cur.execute(sql, (userid,))
        contacts = []
        for row in cur:
            (id,name,phone,email) = row
            contacts.append({
                "id": id,
                "name": name,
                "phone": phone,
                "email": email
            })
        return contacts
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def get_user_by_name(conn, username):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id,name) = row
            return {
                "username": name,
                "userid": id
            }
        else:
            #user does not exist
            return {
                "username": username,
                "userid": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def get_user_by_id(conn, userid):
    """Get user details by id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username FROM users WHERE userid = ?")
        cur.execute(sql, (userid,))
        for row in cur:
            (id,name) = row
            return {
                "username": name,
                "userid": id
            }
        else:
            #user does not exist
            return {
                "username": None,
                "userid": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_hash_for_login(conn, username):
    """Get user details from id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE username=?")
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


if __name__ == "__main__":
    

    try:
        conn = sqlite3.connect("database.db")
    except sqlite3.Error as err:
        print(err)
    else:
        #drop_table(conn)
        create_user_table(conn)
        create_contact_table(conn)
        add_user(conn,"johndoe", generate_password_hash("Joe123"))
        add_user(conn,"maryjane", generate_password_hash("LoveDogs"))
        
        insert_contact(conn, "Don John", "don.john@ymail.com", "12-322-622", 1)
        insert_contact(conn, "Don John", "don.john@ymail.com", "12-322-622", 2)
        insert_contact(conn, "Julia Gucwa", "gucci@outlook.com", "66-112-312", 1)
        insert_contact(conn, "John Smith", "john.smith@gmail.com", "12-345-678", 1)
        insert_contact(conn, "Mario", "+31 997-11-21", "mario@mail.com", 1)
        
        hash = get_hash_for_login(conn, "maryjane")
        print("Check password: {}".format(check_password_hash(hash,"LoveDogs")))
        
        conn.close()