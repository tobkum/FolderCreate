import customtkinter as ctk
import os
import yaml

version = "0.1"

templates = []
newpaths = []

default_path = "X:/Geteilte Ablagen/"
template_path = os.path.join(os.getcwd(), "templates")
for file in os.listdir(template_path):
    if file.endswith(".yaml"):
        templates.append(file)


def dict_to_dir(data, top_path=""):
    if isinstance(data, dict):
        for k, v in data.items():
            dict_to_dir(v, os.path.join(top_path, k))
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                for k, v in i.items():
                    dict_to_dir(v, os.path.join(top_path, k))
            else:
                newpaths.append(os.path.join(top_path, i))


def choose_directory():
    directory = ctk.filedialog.askdirectory(initialdir=default_path)
    if directory:
        root_path_entry.delete(0, ctk.END)
        root_path_entry.insert(0, directory)


def create_folders():
    template = template_combobox.get()
    root_path = root_path_entry.get()
    with open(os.path.join(template_path, template), "r") as stream:
        data = yaml.safe_load(stream)
        dict_to_dir(data)
    for i in newpaths:
        try:
            os.makedirs(os.path.join(root_path, i), exist_ok=True)
        except Exception:
            info_label.configure(text="An error occurred, please check if the directory is writable.", text_color="red")
        else:
            info_label.configure(text="Done", text_color="green")
    info_window.deiconify()


def close_info_window():
    info_window.withdraw()


# Main Application Window
app = ctk.CTk()
app.title("Overmind Studios FolderCreate " + version)
app.geometry("600x400")
app.resizable(False, False) # Prevent window resizing
app.iconbitmap("assets/graphics/appicon.ico")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(3, weight=1)

# Directory Selection Frame
directory_frame = ctk.CTkFrame(app)
directory_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
directory_frame.grid_columnconfigure(0, weight=1)

root_path_entry = ctk.CTkEntry(directory_frame, width=400, placeholder_text="Select Directory")
root_path_entry.insert(0, default_path)
root_path_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

choose_dir_button = ctk.CTkButton(directory_frame, text="Browse", command=choose_directory)
choose_dir_button.grid(row=0, column=1, padx=(0, 0), pady=10)

# Template Selection Combobox
template_combobox = ctk.CTkComboBox(app, values=templates, state="readonly")
template_combobox.set(templates[0])
template_combobox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# Create Folders Button
create_folders_button = ctk.CTkButton(app, text="Create Folders", command=create_folders, height=40, font=("Arial", 16, "bold"))
create_folders_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

# Copyright and Version Labels
copyright_label = ctk.CTkLabel(app, text="© 2025 Overmind Studios - Kummer & Gerhardt GbR", font=("Arial", 10))
copyright_label.grid(row=4, column=0, pady=(10, 5))

version_label = ctk.CTkLabel(app, text="version " + version, font=("Arial", 10))
version_label.grid(row=5, column=0, pady=(0, 20))

# Info Message Popup Window
info_window = ctk.CTkToplevel(app)
info_window.title("Info")
info_window.geometry("300x150")
info_window.withdraw()

info_frame = ctk.CTkFrame(info_window)
info_frame.pack(pady=20, padx=20)

info_label = ctk.CTkLabel(info_frame, text="ERROR")
info_label.pack(pady=10)

ok_button = ctk.CTkButton(info_frame, text="OK", command=close_info_window)
ok_button.pack()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.mainloop()