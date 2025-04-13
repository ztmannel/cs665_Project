'''
Zach Mannel
employee management system interface
#OPTIONAL TODO: move the field horizontal vs the pure vertical trash
'''
import sqlite3
import os
import gui_functions
from conf.config import DB_PATH, DB_SCHEMA

#db_path = DB_PATH
#db_schema = DB_SCHEMA

#check if db has been created
db_file_check = os.path.exists(DB_PATH)

#creates or accesses emp.db
connection = sqlite3.connect(DB_PATH) #create the connection obj
cursor = connection.cursor() #create the cursor obj

#db_file_check:
open_sql_file = open(DB_SCHEMA, "r")
create_sql_file = open_sql_file.read()
#print(create_sql_file)
open_sql_file.close()
#https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
sqlCommands = create_sql_file.split(';')
#create table emp database if it doesnt exist
for command in sqlCommands:
    try:
        cursor.execute(command)
    except sqlite3.OperationalError as oe:
        print(f"Command skipped: {oe}")
#commits the changes to the db
connection.commit()

#passing the path, connection, and cursor so dont need to continuously create
gui_functions.main_gui_shell(DB_PATH, connection, cursor)
#gui_build.delete_tab()

connection.close()
