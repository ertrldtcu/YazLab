import datetime
import sqlite3

con = sqlite3.connect("C:\\Users\\edutc\\Desktop\\YazLab\\II\\I\\database.db", check_same_thread=False)
cur = con.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, username TEXT, password TEXT, login_date TEXT, logout_date '
    'TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS user_car (userid INT, carid INT)')
con.commit()


def login(username, password):
    result = cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password)).fetchone()
    if result:
        return True
    return False


def set_logged_in(username):
    cur.execute("UPDATE users SET login_date=? WHERE username=?", (datetime.datetime.now(), username))
    con.commit()
    return True


def set_logged_out(username):
    cur.execute("UPDATE users SET logout_date=? WHERE username=?", (datetime.datetime.now(), username))
    con.commit()
    return True


def get_id_by_username(username):
    return cur.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()[0]


def get_user_cars(username):
    cars = cur.execute("SELECT carid FROM user_car WHERE userid=?", (get_id_by_username(username),)).fetchall()
    cars = [v[0] for v in cars]
    return cars
