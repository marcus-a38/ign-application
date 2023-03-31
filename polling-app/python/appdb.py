import sqlite3, bcrypt, sys
from datetime import *
from connections import *

PATH = get_db() # <-- get path to database file

# create sqlite db connection

def connect_to_db():

    connection = None

    try:
        connection = sqlite3.connect(PATH)
        return connection
    except sqlite3.Error as e:
        sys.exit(f"Database connection could not be found: {e}")


# get today's date for database entries

def currdate():

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    return date


# post values to the sqlite db

def query_post(sql: str, instance: str, cursor: sqlite3.Cursor):

    query_as_string = fetch_query(sql, instance)

    try:
        cursor.executescript(query_as_string)
    except sqlite3.OperationalError as e:
        sys.exit(f"SQL query encountered problem executing: {e}")


# get values from the sqlite db

def query_get(sql: str, instance: str, cursor: sqlite3.Cursor):


    query_as_string = fetch_query(sql, instance)

    try:
        res = cursor.execute(query_as_string)
    except sqlite3.Error as e:
        sys.exit(f"SQL query encountered problem executing: {e}")

    result = res.fetchall()
    return result


# ---------------------- CLASSES ----------------------- #

class Poll():

    def __init__(self, user_id: str, content: str, options: list):

        self.date = currdate()
        self.uid = user_id
        self.content = content
        self.options = options
        self.pid = None
        self.votes = None
        self.structure = (fr'"{self.uid}"', fr'"{self.content}"', fr'"{self.date}"')


    def __create_options__(self):
        pass


class Option():

    def __init__(self, option_id: str, content: str, poll_id: str):

        self.pid = poll_id
        self.content = content
        self.oid = option_id
        self.votes = None
        self.structure = (fr'"{self.pid}"', fr'"{self.oid}"', fr'"{self.content}"')


class User():

    def __init__(self, username: str, password: str):

        self.username = username
        self.password = password
        self.uid = None
        self.hashedpassword = self.__hash_password__()
        self.accessdate = currdate()
        self.structure = (fr'"{self.username}"', fr'"{self.hashedpassword}"', fr'"{self.accessdate}"')

    def __hash_password__(self):

        password_in_bytes = self.password.encode('utf-8')
        random_salt = bcrypt.gensalt()
        hashedpw = bcrypt.hashpw(password_in_bytes, random_salt)
        return hashedpw.decode('utf-8')


class Vote():

    def __init__(self, user_id: str, poll_id: str, option_id: str):

        self.uid = user_id
        self.pid = poll_id
        self.oid = option_id
        self.structure = (fr'"{self.uid}"', fr'"{self.pid}"', fr'"{self.oid}"')


# compare password input with existing, hashed password ... match -> True, no match -> False

def hash_match(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))