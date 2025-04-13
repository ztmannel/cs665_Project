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
    label1.pack(pady=10)

    #Employee ID search section
    entry_frame = ttk.Frame(parent)
    entry_frame.pack(pady=(5, 10))

    ttk.Label(entry_frame, text="Enter Employee ID:").grid(row=0, column=0, padx=5)
    employee_id_entry = ttk.Entry(entry_frame)
    employee_id_entry.grid(row=0, column=1, padx=5)

    #Search Employee button
    search_btn = ttk.Button(entry_frame, text="Search Employee", command=lambda: search_employee(employee_id_entry.get()))
    search_btn.grid(row=1, column=0, columnspan=2, pady=(5, 10))

    #Scrollable canvas setup
    canvas = tk.Canvas(parent, height=400)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def search_employee(employee_id):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return

        field_map = {}

        def fetch_and_generate_fields(table_name, fields, key_col="employee_id"):
            cursor.execute(f"SELECT * FROM {table_name} WHERE {key_col} = ?", (employee_id,))
            record = cursor.fetchone()
            if not record:
                return

            for idx, field in enumerate(fields, start=1):
                entry_widget = ttk.Entry(scrollable_frame)
                entry_widget.insert(0, record[idx])
                field_map[f"{table_name}.{field}"] = (entry_widget, idx)

        #Fetch main table
        personal_fields = [
            "first_name", "last_name", "position", "phone",
            "address", "city", "state", "country", "personal_email"
        ]
        cursor.execute("SELECT * FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
        employee = cursor.fetchone()
        if not employee:
            msgbox.showerror("Not Found", f"Employee ID {employee_id} not found.")
            return

        for idx, field in enumerate(personal_fields, start=1):
            entry_widget = ttk.Entry(scrollable_frame)
            entry_widget.insert(0, employee[idx])
            field_map[f"employee_personal_info.{field}"] = (entry_widget, idx)

        #Additional tables
        fetch_and_generate_fields("badge_info", ["badge_id", "activation_date", "deactivation_date"])
        fetch_and_generate_fields("compensation_table", ["salary", "bonus", "salary_set_date"])
        fetch_and_generate_fields("employee_company_info", ["company_email", "department", "manager_emp_id", "hire_date", "termination_date"])
        fetch_and_generate_fields("employee_time_off", ["hours_remaining", "hours_consumed", "total_annual_hours"])

        generate_modify_fields(scrollable_frame, field_map)

        save_btn = ttk.Button(scrollable_frame, text="Save Changes", command=lambda: update_employee(field_map))
        save_btn.grid(column=0, row=len(field_map)+1, columnspan=2, pady=(20, 10))

    def generate_modify_fields(frame, field_map):
        for row_idx, (field_name, (entry_widget, _)) in enumerate(field_map.items()):
            label_text = field_name.split('.')[-1].replace('_', ' ').title()
            label = ttk.Label(frame, text=label_text)
            label.grid(row=row_idx, column=0, sticky="e", padx=10, pady=5)
            entry_widget.grid(row=row_idx, column=1, sticky="w", padx=10, pady=5)
    
    #This section is responsible for running the sql update queries
    def update_employee(field_map):
        employee_id = employee_id_entry.get()
        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return

        cursor.execute("SELECT 1 FROM employee_personal_info WHERE employee_id = ?", (employee_id,))
        if not cursor.fetchone():
            msgbox.showerror("Not Found", f"Employee ID {employee_id} not found.")
            return

        updates = {
            "employee_personal_info": [],
            "badge_info": [],
            "compensation_table": [],
            "employee_company_info": [],
            "employee_time_off": []
        }

        for full_key, (entry_widget, _) in field_map.items():
            table, field = full_key.split('.')
            updates[table].append((field, entry_widget.get()))

        for table, fields in updates.items():
            if not fields:
                continue
            set_clause = ", ".join([f"{field} = ?" for field, _ in fields])
            values = [value for _, value in fields]
            where_key = "badge_id" if table == "badge_info" else "employee_id"
            values.append(employee_id)
            cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {where_key} = ?", values)

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
#    build_lookup_tab(lookup_frame, connection, cursor)

    root.mainloop()
