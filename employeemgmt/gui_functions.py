import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
import helper_functions as help
import sqlite3
import csv
from tkinter import filedialog

def build_create_tab(parent, connection, cursor):

    entry_widgets = {}

    #Field definitions not including employee_id - do that separately 
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

    #Add one hidden employee_id entry for each table
    for table_name in static_fields.keys():
        hidden_entry = ttk.Entry(scroll_frame)
        hidden_entry.pack_forget()
        entry_widgets[f"{table_name}.employee_id"] = hidden_entry

    #Field generator for visible fields
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
        #this map will store the values from the select queries
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

        #Fetch main table - employee personal info
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

def build_lookup_tab(parent, connection, cursor):
    label = ttk.Label(parent, text="Lookup Employee Info")
    label.pack(pady=10)

    entry_frame = ttk.Frame(parent)
    entry_frame.pack(pady=(5, 10))

    ttk.Label(entry_frame, text="Enter Employee ID:").grid(row=0, column=0, padx=5)
    employee_id_entry = ttk.Entry(entry_frame)
    employee_id_entry.grid(row=0, column=1, padx=5)

    def list_all_employee_ids():
        cursor.execute("SELECT employee_id FROM employee_personal_info ORDER BY employee_id")
        ids = cursor.fetchall()
        if not ids:
            msgbox.showinfo("No Records", "No employee records found.")
            return

        top = tk.Toplevel()
        top.title("All Employee IDs")

        listbox = tk.Listbox(top, width=40, height=20)
        listbox.pack(padx=10, pady=10)

        for (emp_id,) in ids:
            listbox.insert(tk.END, emp_id)
    def search_employee(employee_id):
        if not employee_id:
            msgbox.showerror("Missing Info", "Please enter an Employee ID.")
            return

        cursor.execute("""
            SELECT p.first_name, p.last_name, p.position, p.phone, p.address,
                    p.city, p.state, p.country, p.personal_email,
                    c.company_email, c.department, c.manager_emp_id, c.hire_date, c.termination_date,
                    t.hours_remaining, t.hours_consumed, t.total_annual_hours
            FROM employee_personal_info p
            LEFT JOIN employee_company_info c ON p.employee_id = c.employee_id
            LEFT JOIN employee_time_off t ON p.employee_id = t.employee_id
            WHERE p.employee_id = ?
        """, (employee_id,))
        result = cursor.fetchone()

        if not result:
            msgbox.showinfo("Not Found", f"No info found for Employee ID {employee_id}")
            return

        top = tk.Toplevel()
        top.title(f"Employee {employee_id} Info")

        labels = [
            "First Name", "Last Name", "Position", "Phone", "Address",
            "City", "State", "Country", "Personal Email",
            "Company Email", "Department", "Manager ID", "Hire Date", "Termination Date",
            "Time Off Remaining", "Time Off Used", "Total Time Off Allowed"
        ]

        for idx, value in enumerate(result):
            ttk.Label(top, text=f"{labels[idx]}:").grid(row=idx, column=0, sticky="w", padx=10, pady=2)
            ttk.Label(top, text=str(value)).grid(row=idx, column=1, sticky="w", padx=10, pady=2)
        
    def show_all_badge_swipes():
        cursor.execute("""
            SELECT first_name, last_name, date_scanned, time_scanned
            FROM employee_personal_info p
            JOIN badge_info b ON p.employee_id = b.employee_id
            JOIN badge_sign_in_times bst ON b.badge_id = bst.badge_id
            ORDER BY date_scanned DESC, time_scanned DESC
        """)
        records = cursor.fetchall()
        if not records:
            msgbox.showinfo("No Records", "No badge swipes found.")
            return

        top = tk.Toplevel()
        top.title("All Badge Swipes")

        tree = ttk.Treeview(top, columns=("first", "last", "date", "time"), show="headings")
        tree.heading("first", text="First Name")
        tree.heading("last", text="Last Name")
        tree.heading("date", text="Date Scanned")
        tree.heading("time", text="Time Scanned")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for row in records:
            tree.insert("", tk.END, values=row)

    def export_to_csv():
        emp_id = employee_id_entry.get().strip()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save As"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                def write_section(header, query, params=()):
                    writer.writerow([header])
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    if not rows:
                        writer.writerow(["No data"])
                        writer.writerow([])
                        return
                    columns = [desc[0] for desc in cursor.description]
                    writer.writerow(columns)
                    writer.writerows(rows)
                    writer.writerow([])  #spacing row

                if emp_id:
                    #Export for a single employee
                    write_section("Employee Personal Info", "SELECT * FROM employee_personal_info WHERE employee_id = ?", (emp_id,))
                    write_section("Badge Info", "SELECT * FROM badge_info WHERE employee_id = ?", (emp_id,))
                    write_section("Compensation Table", "SELECT * FROM compensation_table WHERE employee_id = ?", (emp_id,))
                    write_section("Employee Company Info", "SELECT * FROM employee_company_info WHERE employee_id = ?", (emp_id,))
                    write_section("Employee Time Off", "SELECT * FROM employee_time_off WHERE employee_id = ?", (emp_id,))

                    #Get badge_id and sign-in times
                    cursor.execute("SELECT badge_id FROM badge_info WHERE employee_id = ?", (emp_id,))
                    badge = cursor.fetchone()
                    if badge:
                        badge_id = badge[0]
                        write_section("Badge Sign In Times", "SELECT * FROM badge_sign_in_times WHERE badge_id = ?", (badge_id,))
                else:
                    #Export for all employees
                    write_section("Employee Personal Info", "SELECT * FROM employee_personal_info")
                    write_section("Badge Info", "SELECT * FROM badge_info")
                    write_section("Compensation Table", "SELECT * FROM compensation_table")
                    write_section("Employee Company Info", "SELECT * FROM employee_company_info")
                    write_section("Employee Time Off", "SELECT * FROM employee_time_off")
                    write_section("Badge Sign In Times", "SELECT * FROM badge_sign_in_times")

            msgbox.showinfo("Success", f"Data exported to {file_path}")
        except Exception as e:
            msgbox.showerror("Error", f"Failed to export data.\n{str(e)}")

    #Buttons - they need to come after the function def
    search_btn = ttk.Button(entry_frame, text="Search", command=lambda: search_employee(employee_id_entry.get()))
    search_btn.grid(row=0, column=2, padx=5)

    list_ids_btn = ttk.Button(entry_frame, text="List All Employee IDs", command=list_all_employee_ids)
    list_ids_btn.grid(row=0, column=3, padx=5)

    badge_swipes_btn = ttk.Button(entry_frame, text="Show All Badge Swipes", command=show_all_badge_swipes)
    badge_swipes_btn.grid(row=0, column=4, padx=5)

    export_btn = ttk.Button(entry_frame, text="Export to CSV", command=export_to_csv)
    export_btn.grid(row=0, column=5, padx=5)

def build_delete_tab(parent, connection, cursor):
    label = ttk.Label(parent, text="Delete Employee Record")
    label.pack(pady=10)

    entry_frame = ttk.Frame(parent)
    entry_frame.pack(pady=(5, 10))

    ttk.Label(entry_frame, text="Enter Employee ID:").grid(row=0, column=0, padx=5)
    employee_id_entry = ttk.Entry(entry_frame)
    employee_id_entry.grid(row=0, column=1, padx=5)

    def delete_employee():
        employee_id = employee_id_entry.get()
        if not employee_id:
            msgbox.showerror("Missing Info", "Employee ID is required.")
            return

        # Confirm deletion
        confirm = msgbox.askyesno("Confirm Deletion", f"Are you sure you want to delete Employee ID {employee_id}? This action cannot be undone.")
        if not confirm:
            return

        try:
            # Get badge_id if it exists (used for badge_sign_in_times)
            cursor.execute("SELECT badge_id FROM badge_info WHERE employee_id = ?", (employee_id,))
            badge_row = cursor.fetchone()
            badge_id = badge_row[0] if badge_row else None

            # Delete in reverse dependency order
            if badge_id:
                cursor.execute("DELETE FROM badge_sign_in_times WHERE badge_id = ?", (badge_id,))
            cursor.execute("DELETE FROM badge_info WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM compensation_table WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM employee_company_info WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM employee_time_off WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM employee_personal_info WHERE employee_id = ?", (employee_id,))

            connection.commit()
            msgbox.showinfo("Success", f"Employee ID {employee_id} and related records were deleted.")
            employee_id_entry.delete(0, tk.END)
        except Exception as e:
            msgbox.showerror("Error", f"Failed to delete employee.\n{str(e)}")

    delete_btn = ttk.Button(entry_frame, text="Delete Employee", command=delete_employee)
    delete_btn.grid(row=0, column=2, padx=10)

#THIS IS THE MAIN SHELL FOR THE GUI
def main_gui_shell(DB_PATH, connection, cursor):
    root = tk.Tk()
    root.title("Employee Manager")
    root.geometry("1000x1000")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    #creates the frames for tabs
    create_frame = ttk.Frame(notebook)
    modify_frame = ttk.Frame(notebook)
    lookup_frame = ttk.Frame(notebook)
    delete_frame = ttk.Frame(notebook)

    #tabs and names added here
    notebook.add(create_frame, text="Create")
    notebook.add(modify_frame, text="Modify")
    notebook.add(lookup_frame, text="Lookup")
    notebook.add(delete_frame, text="Delete")

    build_create_tab(create_frame, connection, cursor)
    build_modify_tab(modify_frame, connection, cursor)
    build_lookup_tab(lookup_frame, connection, cursor)
    build_delete_tab(delete_frame, connection, cursor)

    root.mainloop()