import tkinter as tk
from tkinter import filedialog, messagebox, BooleanVar
import json
from backup import BackupManager

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def select_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def run_backup():
    source = entry_source.get()
    dest = entry_dest.get()
    version = entry_version.get()
    zip_option = var_zip.get()

    if not source or not dest:
        messagebox.showerror("Error", "Please select both source and destination folders.")
        return

    bm = BackupManager(source, dest, version, zip_option)
    bm.perform_backup()
    messagebox.showinfo("Done", "Backup completed!")

    save_config({
        "source": source,
        "destination": dest,
        "version": version,
        "zip": zip_option
    })

# GUI
root = tk.Tk()
root.title("Backup Manager")

tk.Label(root, text="Source Folder").grid(row=0, column=0, sticky="e")
entry_source = tk.Entry(root, width=40)
entry_source.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: select_folder(entry_source)).grid(row=0, column=2)

tk.Label(root, text="Destination Folder").grid(row=1, column=0, sticky="e")
entry_dest = tk.Entry(root, width=40)
entry_dest.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: select_folder(entry_dest)).grid(row=1, column=2)

tk.Label(root, text="Version").grid(row=2, column=0, sticky="e")
entry_version = tk.Entry(root, width=40)
entry_version.grid(row=2, column=1)

var_zip = BooleanVar()
tk.Checkbutton(root, text="ZIP Backup", variable=var_zip).grid(row=3, column=1)

tk.Button(root, text="Start Backup", command=run_backup).grid(row=4, column=1, pady=10)

# Load saved config
config = load_config()
entry_source.insert(0, config.get("source", ""))
entry_dest.insert(0, config.get("destination", ""))
entry_version.insert(0, config.get("version", "v1.0"))
var_zip.set(config.get("zip", False))

root.mainloop()
