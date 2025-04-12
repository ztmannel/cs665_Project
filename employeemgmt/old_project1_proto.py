'''
Zach Mannel
employee management system interface
this one populated the fields dynamically by querying the tables
'''
import sqlite3
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk #used for the notebook widget
import os

db_path = "/home/zach/Documents/repos/cs665_Project/dbFiles/emp.db"
db_schema = "/home/zach/Documents/repos/cs665_Project/dbFiles/create.sql"

#check if db has been created
db_file_check = os.path.exists(db_path)

#creates or accesses the existing emp.db
connection = sqlite3.connect(db_path) #create the connection obj
cursor = connection.cursor() #create the cursor obj

#
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

#List of tables in the database
tables = [
    "employee_personal_info",
    "compensation_table",
    "employee_company_info",
    "badge_info"
    #"employee_time_off"    #we'll modify this after the employee has been added
]

#Building the gui based on dynamic fields queried from the database
root = tk.Tk()
root.title("Dynamic Entry Fields")
root.geometry("500x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

create_tab1 = ttk.Frame(notebook)
modify_tab2 = ttk.Frame(notebook)
lookup_tab3 = ttk.Frame(notebook)
notebook.add(create_tab1, text='Create')
notebook.add(modify_tab2, text='Modify')
notebook.add(lookup_tab3, text='Lookup')

# Add content to Tab 1
label1 = ttk.Label(create_tab1, text="Add a new employee")
label1.pack(pady=20)

# Add content to Tab 2
label2 = ttk.Label(modify_tab2, text="Modify an existing employee")
label2.pack(pady=20)

# Add content to Tab 3
label3 = ttk.Label(lookup_tab3, text="Search existing employee data")
label3.pack(pady=20)

#Dictionary to hold generated Entry widgets
entry_widgets = {}

#Function to generate fields in a table
#TODO - need to reduce number of duplicate data entry fields - consolidate them somehow
def generate_fields_for_table(parent_frame, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")   #This is responsible for returning the files in the table
        columns = [desc[0] for desc in cursor.description]

        ttk.Label(parent_frame, text=f"{table_name}", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))

        for col in columns:
            label = ttk.Label(parent_frame, text=col)
            label.pack()
            entry = ttk.Entry(parent_frame)
            entry.pack()
            # Store entry in dictionary for later use
            entry_widgets[f"{table_name}.{col}"] = entry

    except sqlite3.OperationalError as e:
        ttk.Label(parent_frame, text=f"{table_name} not found", foreground="red").pack()

#Create a scrollable frame in the tab
canvas = tk.Canvas(create_tab1)
scrollbar = ttk.Scrollbar(create_tab1, orient="vertical", command=canvas.yview)
scroll_frame = ttk.Frame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

#Generate the fields
for table in tables:
    generate_fields_for_table(scroll_frame, table)

root.mainloop()

connection.close()