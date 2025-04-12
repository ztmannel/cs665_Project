'''
Zach Mannel
employee management system interface
'''
import sqlite3
import os
import gui_functions

db_path = "/home/zach/Documents/repos/cs665_Project/dbFiles/emp.db"
db_schema = "/home/zach/Documents/repos/cs665_Project/dbFiles/create.sql"

#check if db has been created
db_file_check = os.path.exists(db_path)

#creates or accesses the existing emp.db
connection = sqlite3.connect(db_path) #create the connection obj
cursor = connection.cursor() #create the cursor obj

#if not db_file_check:
open_sql_file = open(db_schema, "r")
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
gui_functions.create_tab(db_path, connection, cursor)
#gui_build.modify_tab()
#gui_build.lookup_tab()
#gui_build.delete_tab()

connection.close()
