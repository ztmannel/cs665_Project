#This file contains various helper functions. I could move more from the gui_functions.py, but time constraints. see on_submit for example

from collections import defaultdict
import sqlite3
import tkinter as tk
import tkinter.messagebox as msgbox

#creates the table_data so we can build the sql statements
def group_entries_by_table(entry_widgets):
    table_data = defaultdict(dict)
    for key, widget in entry_widgets.items():
        table_name, field_name = key.split(".")
        table_data[table_name][field_name] = widget.get()
    return table_data

#builds the insert statements based on the input fields
def build_insert_statements(table_data):
    statements = []
    values = []
    
    for table, fields in table_data.items():
        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?" for _ in fields])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        val_tuple = tuple(fields.values())
        statements.append(sql)
        values.append(val_tuple)
    
    return statements, values

#inserts the input data to sql
def insert_all_data(connection, cursor, entry_widgets):
    
    table_data = group_entries_by_table(entry_widgets)
    statements, values = build_insert_statements(table_data)

    #cursor = conn.cursor()
    for sql, val in zip(statements, values):
        cursor.execute(sql, val)
    connection.commit()

#controls the functionality of the submit button
def on_submit(employee_id_entry, entry_widgets, connection, cursor):
    employee_id = employee_id_entry.get()
    #will pop a dialog for employee id
    if not employee_id:
        msgbox.showerror("Missing Info", "Employee ID is required.")
        return
    #check for existing employee_id. using ? will prevent sql injection via parameter
    cursor.execute("SELECT 1 FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
    if cursor.fetchone():
        msgbox.showerror("Invalid Entry", f"Employee ID {employee_id} already exists")
        return

    #Inject into all hidden fields regardless of table name to prevent duplicate or conflicting inputs
    for key in entry_widgets:
        if key.endswith(".employee_id"):
            entry_widgets[key].delete(0, tk.END)
            entry_widgets[key].insert(0, employee_id)

    insert_all_data(connection, cursor, entry_widgets)
    connection.commit()
    msgbox.showinfo("Success", "Employee added to system successfully.")

def clear_fields(employee_id_entry, entry_widgets):
    for widget in entry_widgets.values():
        widget.delete(0, tk.END)
    employee_id_entry.delete(0, tk.END)