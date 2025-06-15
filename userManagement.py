import sqlite3 as sql
import bcrypt

def checkAdmin(username, password):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_users WHERE admin_user=?", (username,))
    user = cur.fetchone() 
    if user:
        stored_password = user[2] 
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True
        else:
            return False
    else:
        return False

def changePassword(username, new_password):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cur.execute("UPDATE admin_users SET password=? WHERE admin_user=?", (hashed, username))
    con.commit()
    con.close()

def validate_password(password: str) -> dict:
    errors = {
        'length': False,
        'upper': False,
        'lower': False,
        'number': False,
        'special': False,
        'duplicate': False,
    }
    if len(password) < 8:
        errors['length'] = True
    if not any(char.isupper() for char in password):
        errors['upper'] = True
    if not any(char.islower() for char in password):
        errors['lower'] = True
    if not any(char.isdigit() for char in password):
        errors['number'] = True
    if not any(char in '!@#$%^&*' for char in password):
        errors['special'] = True
    return errors


def getAdminEmail(username):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_users WHERE admin_user=?", (username,))
    user = cur.fetchone() 
    if user:
        return user[3] 
    else:
        return None