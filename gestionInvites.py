import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_table():
    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

def validate_name(name):
    return name.isalpha() and len(name) > 0

def validate_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) >= 10

def add_person():
    person_id = entry_person_id.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone_number = entry_phone_number.get()

    if not person_id.isdigit() or not validate_name(first_name) or not validate_name(last_name) or not validate_phone_number(phone_number):
        messagebox.showwarning("Warning", "Invalid input. Please enter valid values.")
        return

    person_id = int(person_id)

    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM people WHERE id=?", (person_id,))
    existing_id = cursor.fetchone()

    if existing_id:
        messagebox.showwarning("Warning", f"Person with ID {person_id} already exists. Please choose a different ID.")
    else:
        cursor.execute("INSERT INTO people (id, first_name, last_name, phone_number) VALUES (?, ?, ?, ?)",
                       (person_id, first_name, last_name, phone_number))

        connection.commit()
        connection.close()

        entry_person_id.delete(0, tk.END)
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_phone_number.delete(0, tk.END)

        display_people()

        messagebox.showinfo("Success", "Person added successfully!")

def delete_person():
    person_id = entry_delete_id.get()

    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM people WHERE id=?", (person_id,))
    existing_person = cursor.fetchone()

    if existing_person:
        cursor.execute("DELETE FROM people WHERE id=?", (person_id,))
        connection.commit()
        connection.close()

        entry_delete_id.delete(0, tk.END)

        display_people()

        messagebox.showinfo("Success", "Person deleted successfully!")
    else:
        messagebox.showwarning("Warning", "Person does not exist in the database.")

def modify_person():
    person_id = entry_modify_id.get()
    new_first_name = entry_new_first_name.get()
    new_last_name = entry_new_last_name.get()
    new_phone_number = entry_new_phone_number.get()

    if not person_id.isdigit() or not validate_name(new_first_name) or not validate_name(new_last_name) or not validate_phone_number(new_phone_number):
        messagebox.showwarning("Warning", "Invalid input for new information. Please enter valid values.")
        return

    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM people WHERE id=?", (person_id,))
    existing_person = cursor.fetchone()

    if existing_person:
        cursor.execute("UPDATE people SET first_name=?, last_name=?, phone_number=? WHERE id=?",
                       (new_first_name, new_last_name, new_phone_number, person_id))
        connection.commit()
        connection.close()

        entry_modify_id.delete(0, tk.END)
        entry_new_first_name.delete(0, tk.END)
        entry_new_last_name.delete(0, tk.END)
        entry_new_phone_number.delete(0, tk.END)

        display_people()

        messagebox.showinfo("Success", "Person modified successfully!")
    else:
        messagebox.showwarning("Warning", "Person does not exist in the database.")

def verify_person():
    person_id = entry_verify_id.get()

    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute("SELECT first_name, last_name FROM people WHERE id=?", (person_id,))
    existing_person = cursor.fetchone()

    connection.close()

    if existing_person:
        first_name, last_name = existing_person
        messagebox.showinfo("Verification", f"Person with ID {person_id} exists in the database.\nName: {first_name} {last_name}")
    else:
        messagebox.showinfo("Verification", f"Person with ID {person_id} does not exist in the database.")

def display_people():
    connection = sqlite3.connect("invited_people.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM people")
    people = cursor.fetchall()

    connection.close()

    for row in display_tree.get_children():
        display_tree.delete(row)

    for person in people:
        display_tree.insert("", "end", values=person)

root = tk.Tk()
root.title("Invited People Management")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))

tree_font = ("Helvetica", 10)
style.configure("Treeview.Heading", font=tree_font)
style.configure("Treeview", font=tree_font)

create_table()

root.configure(bg="#5FBDFF")

title_style = ttk.Style()
title_style.configure("Title.TLabel", font=("Helvetica", 14), background="#96EFFF", padding=5)

add_title = ttk.Label(root, text="ADD", style="Title.TLabel", anchor="center")
add_title.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
tk.Label(root, text="ID:", font=("Helvetica", 12), bg="#96EFFF").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="First Name:", font=("Helvetica", 12), bg="#96EFFF").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="Last Name:", font=("Helvetica", 12), bg="#96EFFF").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="Phone Number:", font=("Helvetica", 12), bg="#96EFFF").grid(row=4, column=0, sticky="e", padx=5, pady=5)

entry_person_id = tk.Entry(root, font=("Helvetica", 12))
entry_first_name = tk.Entry(root, font=("Helvetica", 12))
entry_last_name = tk.Entry(root, font=("Helvetica", 12))
entry_phone_number = tk.Entry(root, font=("Helvetica", 12))

entry_person_id.grid(row=1, column=1, sticky="w", padx=5, pady=5)
entry_first_name.grid(row=2, column=1, sticky="w", padx=5, pady=5)
entry_last_name.grid(row=3, column=1, sticky="w", padx=5, pady=5)
entry_phone_number.grid(row=4, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Add Person", command=add_person, bg="#C5FFF8").grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")

ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)

delete_title = ttk.Label(root, text="DELETE", style="Title.TLabel", anchor="center")
delete_title.grid(row=7, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
tk.Label(root, text="Person ID:", font=("Helvetica", 12), bg="#96EFFF").grid(row=8, column=0, sticky="e", padx=5, pady=5)

entry_delete_id = tk.Entry(root, font=("Helvetica", 12))
entry_delete_id.grid(row=8, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Delete Person", command=delete_person, bg="#C5FFF8").grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")

ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=10, column=0, columnspan=2, sticky="ew", pady=5)

modify_title = ttk.Label(root, text="MODIFY", style="Title.TLabel", anchor="center")
modify_title.grid(row=11, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
tk.Label(root, text="Person ID:", font=("Helvetica", 12), bg="#96EFFF").grid(row=12, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="New First Name:", font=("Helvetica", 12), bg="#96EFFF").grid(row=13, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="New Last Name:", font=("Helvetica", 12), bg="#96EFFF").grid(row=14, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="New Phone Number:", font=("Helvetica", 12), bg="#96EFFF").grid(row=15, column=0, sticky="e", padx=5, pady=5)

entry_modify_id = tk.Entry(root, font=("Helvetica", 12))
entry_new_first_name = tk.Entry(root, font=("Helvetica", 12))
entry_new_last_name = tk.Entry(root, font=("Helvetica", 12))
entry_new_phone_number = tk.Entry(root, font=("Helvetica", 12))

entry_modify_id.grid(row=12, column=1, sticky="w", padx=5, pady=5)
entry_new_first_name.grid(row=13, column=1, sticky="w", padx=5, pady=5)
entry_new_last_name.grid(row=14, column=1, sticky="w", padx=5, pady=5)
entry_new_phone_number.grid(row=15, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Modify Person", command=modify_person, bg="#C5FFF8").grid(row=16, column=0, columnspan=2, pady=10, sticky="nsew")

ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=17, column=0, columnspan=2, sticky="ew", pady=5)

verify_title = ttk.Label(root, text="VERIFY", style="Title.TLabel", anchor="center")
verify_title.grid(row=18, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
tk.Label(root, text="Person ID:", font=("Helvetica", 12), bg="#96EFFF").grid(row=19, column=0, sticky="e", padx=5, pady=5)

entry_verify_id = tk.Entry(root, font=("Helvetica", 12))
entry_verify_id.grid(row=19, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Verify Person", command=verify_person, bg="#C5FFF8").grid(row=20, column=0, columnspan=2, pady=10, sticky="nsew")

display_frame = tk.Frame(root, bg="#ffffff")
display_frame.grid(row=0, column=5, rowspan=22, padx=10, pady=10, sticky="nsew")

display_tree = ttk.Treeview(display_frame, columns=("ID", "First Name", "Last Name", "Phone Number"), show="headings")
display_tree.heading("ID", text="ID")
display_tree.heading("First Name", text="First Name")
display_tree.heading("Last Name", text="Last Name")
display_tree.heading("Phone Number", text="Phone Number")

vsb = ttk.Scrollbar(display_frame, orient="vertical", command=display_tree.yview)
vsb.pack(side="right", fill="y")
display_tree.configure(yscrollcommand=vsb.set)

display_tree.pack(expand=True, fill="both")

display_people()

for i in range(6):
    root.grid_columnconfigure(i, weight=1)

for i in range(22):
    root.grid_rowconfigure(i, weight=1)

root.mainloop()
