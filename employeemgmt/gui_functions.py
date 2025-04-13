import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
import helper_functions as help
import sqlite3

def build_create_tab(parent, connection, cursor):

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

    #Scrollable canvas
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #Single employee_id entry shown at the top
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

    submit_btn = ttk.Button(scroll_frame, text="Submit", command=lambda: help.on_submit(employee_id_entry, entry_widgets, connection, cursor))
    submit_btn.pack(pady=20)
    
    #button to actually clear the fields
    clear_btn = ttk.Button(scroll_frame, text="Clear", command=lambda: help.clear_fields(employee_id_entry, entry_widgets, connection, cursor))
    clear_btn.pack(pady=(0, 10))

def build_modify_tab(parent, connection, cursor):
    label1 = ttk.Label(parent, text="Modify Employee Info")
    label1.pack(pady=20)
    
    #Enter Employee ID to search for an employee
    ttk.Label(parent, text="Enter Employee ID").pack(pady=(10, 0))
    employee_id_entry = ttk.Entry(parent)
    employee_id_entry.pack(pady=(5, 10))
    
    #Button to trigger search
    def search_employee():
        employee_id = employee_id_entry.get()
        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return
        
        cursor.execute("SELECT * FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
        employee = cursor.fetchone()

        if not employee:
            msgbox.showerror("Not Found", f"Employee ID {employee_id} not found.")
            return

        #Create the entry widgets dynamically
        first_name = ttk.Entry(parent)
        last_name = ttk.Entry(parent)
        position = ttk.Entry(parent)
        phone = ttk.Entry(parent)
        address = ttk.Entry(parent)
        city = ttk.Entry(parent)
        state = ttk.Entry(parent)
        country = ttk.Entry(parent)
        personal_email = ttk.Entry(parent)

        #Map field names to their respective indices
        fields = [
            ("first_name", 1),
            ("last_name", 2),
            ("position", 3),
            ("phone", 4),
            ("address", 5),
            ("city", 6),
            ("state", 7),
            ("country", 8),
            ("personal_email", 9)
        ]

        field_map = {}

        #Loop through each entry widget and fill corresponding value
        for field_name, index in fields:
            entry_widget = ttk.Entry(parent)
            entry_widget.insert(0, employee[index])
            field_map[field_name] = (entry_widget, index)
        
        generate_modify_fields(parent, field_map)

        save_btn = ttk.Button(parent, text="Save Changes", command=lambda: update_employee(field_map))
        save_btn.pack(pady=(10, 20))

    search_btn = ttk.Button(parent, text="Search Employee", command=search_employee)
    search_btn.pack(pady=(5, 10))
    
    #Display Fields to Modify (Assuming employee info fields)
    #These fields are where the user will modify data

    def generate_modify_fields(parent_frame, field_map):
        for field_name, (entry_widget, _) in field_map.items():
            label = ttk.Label(parent_frame, text=field_name.replace('_', ' ').title())
            label.pack(pady=(5, 0))
            entry_widget.pack(pady=(5, 10))
    
    #Save changes back to the database
    def update_employee(field_map):
        employee_id = employee_id_entry.get()
        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return
        
        cursor.execute("SELECT 1 FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
        if not cursor.fetchone():
            msgbox.showerror("Not Found", f"Employee ID {employee_id} not found.")
            return
        
        #Use [0] to access the entry widget in each tuple
        first_name = field_map["first_name"][0].get()
        last_name = field_map["last_name"][0].get()
        position = field_map["position"][0].get()
        phone = field_map["phone"][0].get()
        address = field_map["address"][0].get()
        city = field_map["city"][0].get()
        state = field_map["state"][0].get()
        country = field_map["country"][0].get()
        personal_email = field_map["personal_email"][0].get()

        #Update the employee in the database
        cursor.execute("""
            UPDATE employee_personal_info
            SET first_name = ?, last_name = ?, position = ?, phone = ?, address = ?, city = ?, state = ?, country = ?, personal_email = ?
            WHERE employee_id = ?
        """, (first_name, last_name, position, phone, address, city, state, country, personal_email, employee_id))
        
        connection.commit()
        msgbox.showinfo("Success", "Employee information updated successfully.")
    

#THIS IS THE MAIN SHELL FOR THE GUI
def main_gui_shell(DB_PATH, connection, cursor):
    root = tk.Tk()
    root.title("Employee Manager")
    root.geometry("1400x1000")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    #creates the frames for tabs
    create_frame = ttk.Frame(notebook)
    modify_frame = ttk.Frame(notebook)
    lookup_frame = ttk.Frame(notebook)
    #tabs and names added here
    notebook.add(create_frame, text="Create")
    notebook.add(modify_frame, text="Modify")
    notebook.add(lookup_frame, text="Lookup")

    build_create_tab(create_frame, connection, cursor)
    build_modify_tab(modify_frame, connection, cursor)
    # populate_lookup_tab(lookup_frame, connection, cursor)  # optional

    root.mainloop()
