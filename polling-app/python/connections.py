import os.path, sys
from query_strings import *

written_by = "marcus antonelli"
final_v_date = "3/29/2023"

# create database connections

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)  # change dirname based on type, .exe or .py
elif __file__:
    app_path = os.path.dirname(os.path.abspath(__file__))

sql_path = os.path.join(app_path, "sqlite")
filepath =  os.path.join(sql_path, "queries", "queries.sql")

query_dict = get_query_strings(filepath) # get the SQL query strings from query_strings.py dict

# fetch database via path
def get_db():
    return os.path.join(sql_path, "main.db")

# fetch .ui file via path
def connect_to_ui():
    return os.path.join(app_path, 'python', 'app.ui')

#fetch 
def fetch_query(query_type, values):

    try:
        query_index = query_dict[query_type]
    except KeyError as e:
        sys.exit(f"Invalid query type: {e}")

    sql_script = query_index[0]

    if query_index[1] is not None: # some queries will not require any string interpolation, these will be type None.

        replace_letters = query_index[1]
        letters = iter(replace_letters)
        replace = iter(values)
        query_as_string = sql_script

        for x in letters: # insert the values into the query
            temp = str(next(replace))
            query_as_string = query_as_string.replace(x, temp)
        return query_as_string
    
    else: # so, if the query has a None type 'instance' object, just fetch the string as is.
        return query_index[0]