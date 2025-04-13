import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
import helper_functions
import sqlite3
#import os

def create_tab(DB_PATH, connection, cursor):
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

    entry_widgets = {}

    # Field definitions without employee_id
    emp_personal_info_fields = [
        "first_name", "last_name", "position", "phone",
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

    employee_time_off_fields = [
        "hours_remaining", "hours_consumed", "total_annual_hours"
    ]

    static_fields = {
        "employee_personal_info": emp_personal_info_fields,
        "compensation_table": compensation_table_fields,
        "employee_company_info": emp_company_info_fields,
        "badge_info": badge_info_fields,
        "employee_time_off": employee_time_off_fields
    }

    # Scrollable canvas
    canvas = tk.Canvas(create_tab)
    scrollbar = ttk.Scrollbar(create_tab, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Single employee_id entry shown at the top
    ttk.Label(scroll_frame, text="Employee ID", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
    employee_id_entry = ttk.Entry(scroll_frame)
    employee_id_entry.pack()

    # Add one hidden employee_id entry for each table
    for table_name in static_fields.keys():
        hidden_entry = ttk.Entry(scroll_frame)
        hidden_entry.pack_forget()
        entry_widgets[f"{table_name}.employee_id"] = hidden_entry

    # Field generator for visible fields
    def generate_static_fields(parent_frame, table_name, fields):
        ttk.Label(parent_frame, text=f"{table_name}", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
        for field in fields:
            label = ttk.Label(parent_frame, text=field)
            label.pack()
            entry = ttk.Entry(parent_frame)
            entry.pack()
            entry_widgets[f"{table_name}.{field}"] = entry

    for table_name, fields in static_fields.items():
        generate_static_fields(scroll_frame, table_name, fields)

    def on_submit():
        employee_id = employee_id_entry.get()
        #will pop a dialog for employee id
        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return
        #check for existing employee_id. using ? will prevent sql injection via parameter
        cursor.execute("SELECT 1 FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
        if cursor.fetchone():
            msgbox.showerror("Invalid Entry", "Employee ID {employee_id} already exists")
            return

        #Inject into all hidden fields regardless of table name to prevent duplicate or conflicting inputs
        for key in entry_widgets:
            if key.endswith(".employee_id"):
                entry_widgets[key].delete(0, tk.END)
                entry_widgets[key].insert(0, employee_id)

        helper_functions.insert_all_data(connection, cursor, entry_widgets)
        connection.commit()
        print("User Added Successfully")

    submit_btn = ttk.Button(scroll_frame, text="Submit", command=on_submit)
    submit_btn.pack(pady=20)

    root.mainloop()
