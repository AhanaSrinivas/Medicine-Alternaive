import tkinter as tk
from tkinter import messagebox
import csv

def load_medicine_data(filename):
    medicine_db = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["Medicine"].strip() if "Medicine" in row else row["Component"].strip()
            if key not in medicine_db:
                medicine_db[key] = []
            medicine_db[key].append({
                "component": row["Component"],
                "alternative": row["Alternative"],
                "price": int(row['Price'])
            })
    return medicine_db

def update_checkboxes():
    search_term = entry_var.get().strip().lower()
    for widget in check_frame.winfo_children():
        widget.destroy()
    
    matching_medicines = [med for med in medicine_db.keys() if med.lower().startswith(search_term)]
    
    for med in matching_medicines:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(check_frame, text=med, variable=var, command=lambda m=med: set_selected_medicine(m))
        chk.var = var
        chk.pack(anchor='w')

def set_selected_medicine(med):
    entry_var.set(med)

def find_alternative():
    selected_medicine = entry_var.get().strip()
    if selected_medicine in medicine_db:
        alternatives = sorted(medicine_db[selected_medicine], key=lambda x: x["price"])
        result_text = "\n".join([f"{alt['alternative']} - ₹{alt['price']}" for alt in alternatives])
        result_label.config(text=result_text)
    else:
        messagebox.showerror("Error", "Medicine not found in database")

def search_window(csv_file, title):
    global medicine_db, entry_var, check_frame, result_label
    medicine_db = load_medicine_data(csv_file)
    
    search_root = tk.Tk()
    search_root.title(title)
    search_root.geometry("400x500")
    
    tk.Label(search_root, text=title, font=("Arial", 12, "bold")).pack(pady=10)
    
    entry_var = tk.StringVar()
    entry = tk.Entry(search_root, textvariable=entry_var, width=30)
    entry.pack(pady=5)
    entry_var.trace("w", lambda *args: update_checkboxes())
    
    check_frame = tk.Frame(search_root)
    check_frame.pack(pady=10)
    
    search_button = tk.Button(search_root, text="Find Alternative", command=find_alternative)
    search_button.pack(pady=10)
    
    result_label = tk.Label(search_root, text="", fg="blue", font=("Arial", 12))
    result_label.pack(pady=10)
    
    back_button = tk.Button(search_root, text="Back", command=search_root.destroy)
    back_button.pack(pady=10)
    
    search_root.mainloop()

def main_menu():
    global root
    root = tk.Tk()
    root.title("Indian Medical AI")
    root.geometry("400x300")
    
    def show_options():
        start_button.pack_forget()
        search_by_name_button.pack(pady=10)
        search_by_composition_button.pack(pady=10)
    
    tk.Label(root, text="Welcome to Indian Medical AI", font=("Arial", 14, "bold")).pack(pady=20)
    
    start_button = tk.Button(root, text="Get Started", command=show_options, width=25)
    start_button.pack(pady=10)
    
    search_by_name_button = tk.Button(root, text="Search by Medicine Name", command=lambda: [root.destroy(), search_window("medicine_data3.csv", "Select Medicine Name")], width=25)
    search_by_composition_button = tk.Button(root, text="Search by Composition", command=lambda: [root.destroy(), search_window("medicine_data2.csv", "Select Composition")], width=25)
    
    root.mainloop()

main_menu()
