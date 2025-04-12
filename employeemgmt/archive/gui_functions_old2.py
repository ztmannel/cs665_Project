import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk #used for the notebook widget
import helper_functions
import sqlite3
import os 

def create_tab():
    root = tk.Tk()
    root.title("Employee Manager")
    root.geometry("500x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    create_tab = ttk.Frame(notebook)
    modify_tab = ttk.Frame(notebook)
    lookup_tab = ttk.Frame(notebook)

    notebook.add(create_tab, text='Create')
    notebook.add(modify_tab, text='Modify')
    notebook.add(lookup_tab, text='Lookup')

    label1 = ttk.Label(create_tab, text="Add a new employee")
    label1.pack(pady=20)

    #Field definitions and entry points
    entry_widgets = {}

    #Individual field lists
    emp_personal_info_fields_id = [
        "employee_id"
    ]

    emp_personal_info_fields = [
        "first_name", "last_name", "position", "phone xxx-xxx-xxxx",
        "address", "city", "state", "country", "personal_email"
    ]

    compensation_table_fields = [
        "salary", "bonus", "salary_set_date"
    ]

    emp_company_info_fields = [
        "company_email", "department", "manager_emp_id",
        "hire_date", "termination_date"
    ]

    badge_info_fields = [
        "badge_id", "activation_date", "deactivation_date"
    ]

    #Build the static_fields dictionary using the variables
    static_fields = {
        "employee_id": emp_personal_info_fields_id,
        "employee_personal_info": emp_personal_info_fields,
        "compensation_table": compensation_table_fields,
        "employee_company_info": emp_company_info_fields,
        "badge_info": badge_info_fields
    }

    def generate_static_fields(parent_frame, table_name, fields):
        ttk.Label(parent_frame, text=f"{table_name}", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
        for field in fields:
            label = ttk.Label(parent_frame, text=field)
            label.pack()
            entry = ttk.Entry(parent_frame)
            entry.pack()
            entry_widgets[f"{table_name}.{field}"] = entry

    #Scrollable canvas
    canvas = tk.Canvas(create_tab)
    scrollbar = ttk.Scrollbar(create_tab, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #Generate fields for each table
    for table_name, fields in static_fields.items():
        generate_static_fields(scroll_frame, table_name, fields)
    
    db_path = "/home/zach/Documents/repos/cs665_Project/dbFiles/emp.db"
    connection = sqlite3.connect(db_path) #create the connection obj
    cursor = connection.cursor() #create the cursor obj

    #Will insert the input data into the database
    def on_submit(entry_widgets):
        helper_functions.insert_all_data(p1.cursor, entry_widgets)
        connection.commit()
        print("User Added Successfully")

    #Basic submit button
    submit_btn = ttk.Button(scroll_frame, text="Submit", command=on_submit)
    submit_btn.pack(pady=20)

    root.mainloop()