#This file will contain various helper functions

from collections import defaultdict
import sqlite3

def group_entries_by_table(entry_widgets):
    table_data = defaultdict(dict)
    for key, widget in entry_widgets.items():
        table_name, field_name = key.split(".")
        table_data[table_name][field_name] = widget.get()
    return table_data

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

def insert_all_data(conn, entry_widgets):
    table_data = group_entries_by_table(entry_widgets)
    statements, values = build_insert_statements(table_data)

    cursor = conn.cursor()
    for sql, val in zip(statements, values):
        cursor.execute(sql, val)
    conn.commit()
