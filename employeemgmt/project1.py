'''
Zach Mannel
employee management system interface
'''
import sqlite3
import tkinter as tk
import tkinter.messagebox as msgbox

connection = sqlite3.connect("/home/zach/Documents/repos/cs665_Project/dbFiles/emp.db") #create the connection obj
cursor = connection.cursor() #create the cursor obj

#Open the sql file
open_sql_file = open("/home/zach/Documents/repos/cs665_Project/dbFiles/create.sql", "r")
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

#init tk gui
root = tk.Tk()
root.title("EMDB")

#textbox to display results
textBox = tk.Text(root, height=20, width=60)
textBox.pack()

#create text entry box with a label
textLabel = tk.Label(root, text = "Test EMDB:")
textLabel.pack()
textEntry = tk.Entry(root)
textEntry.pack()

root.mainloop()

connection.close()