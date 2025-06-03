import sqlite3 as sql
import bcrypt



def checkAdmin(username, password):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_users WHERE admin_user=?", (username,))
    user = cur.fetchone() 
    if user:
        stored_password = user[2] 
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
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



def getAdminEmail(username):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_users WHERE admin_user=?", (username,))
    user = cur.fetchone() 
    if user:
        return user[3] 
    else:
        return None


def main():
    password = "P@ssword123"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(hashed)
    print(bcrypt.checkpw(password.encode('utf-8'), hashed))
if __name__ == "__main__":
    main()