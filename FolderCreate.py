import customtkinter as ctk
import os
import yaml

version = "0.3"

# Global variable to store the last created root path
last_created_root_path = None

# --- Constants and Setup ---
DEFAULT_PATH_FILE = "default_path.txt"
DEFAULT_PATH = "X:/Geteilte Ablagen/"  # Fallback default path
TEMPLATE_PATH = os.path.join(os.getcwd(), "templates")


def close_info_window():
    info_window.withdraw()


def close_preview_window():
    preview_window.withdraw()


def load_default_path():
    """Loads the default path from a file, or returns the hardcoded default."""
    try:
        with open(DEFAULT_PATH_FILE, "r") as f:
            path = f.read().strip()
            if os.path.isdir(path):
                return path
    except FileNotFoundError:
        pass  # File doesn't exist, use hardcoded default
    return DEFAULT_PATH


def save_default_path(path):
    """Saves the given path as the new default path."""
    try:
        with open(DEFAULT_PATH_FILE, "w") as f:
            f.write(path)
        return True
    except Exception as e:
        print(f"Error saving default path: {e}")
        return False


def load_templates(path):
    """Scans the template directory for .yaml files, returning a sorted list."""
    if not os.path.isdir(path):
        return []
    try:
        return sorted([f for f in os.listdir(path) if f.endswith((".yaml", ".yml"))])
    except OSError as e:
        print(f"Error reading template directory {path}: {e}")
        return []


def _generate_paths_from_template_data(data, current_path=""):
    """
    Recursively traverses the YAML data structure and returns a list of full directory paths.
    This is a refactored, side-effect-free version of the original dict_to_dir logic.
    """
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            paths.extend(
                _generate_paths_from_template_data(
                    value, os.path.join(current_path, key)
                )
            )
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    paths.extend(
                        _generate_paths_from_template_data(
                            value, os.path.join(current_path, key)
                        )
                    )
            else:
                paths.append(os.path.join(current_path, str(item)))
    return paths


def choose_directory():
    """Opens a dialog to choose the root directory for folder creation."""
    directory = ctk.filedialog.askdirectory(initialdir=root_path_entry.get())
    if directory:
        root_path_entry.delete(0, ctk.END)
        root_path_entry.insert(0, directory)


def set_default_path():
    """Sets the currently selected directory as the new default path."""
    current_path = root_path_entry.get()
    if os.path.isdir(
        current_path
    ):  # Check if the path in the entry is a valid directory
        if save_default_path(current_path):
            info_label.configure(
                text=f"Default path set to: {current_path}", text_color="green"
            )
        else:
            info_label.configure(text="Failed to save default path.", text_color="red")
    else:
        info_label.configure(
            text="Invalid path in entry. Please select a valid directory first.",
            text_color="orange",
        )
    info_window.deiconify()

    # Position the info window relative to the main window
    x = app.winfo_x() + app.winfo_width() // 2 - info_window.winfo_width() // 2
    y = app.winfo_y() + app.winfo_height() // 2 - info_window.winfo_height() // 2
    info_window.geometry(f"+{x}+{y}")


def create_folders():
    """Main function to orchestrate folder creation based on UI selections."""
    root_path = root_path_entry.get()
    template_name = template_combobox.get()
    template_file_path = os.path.join(TEMPLATE_PATH, template_name)

    # --- 1. Load and Parse Template ---
    try:
        with open(template_file_path, "r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except FileNotFoundError:
        info_label.configure(
            text=f"Error: Template file '{template_name}' not found.", text_color="red"
        )
        info_window.deiconify()
        return
    except yaml.YAMLError as e:
        info_label.configure(text=f"Error parsing template: {e}", text_color="red")
        info_window.deiconify()
        return
    except Exception as e:
        info_label.configure(
            text=f"An unexpected error occurred: {e}", text_color="red"
        )
        info_window.deiconify()
        return

    # --- 2. Generate Paths ---
    if data is None:
        info_label.configure(text="Template file is empty.", text_color="orange")
        info_window.deiconify()
        return

    paths_to_create = _generate_paths_from_template_data(data)

    if not paths_to_create:
        info_label.configure(
            text="Template is valid, but contains no folders to create.",
            text_color="orange",
        )
        info_window.deiconify()
        return

    # --- 3. Create Directories ---
    errors_occurred = False
    for path_suffix in paths_to_create:
        try:
            full_path = os.path.join(root_path, path_suffix)
            os.makedirs(full_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {full_path}: {e}")
            errors_occurred = True

    if errors_occurred:
        info_label.configure(
            text="An error occurred. Check console for details.",
            text_color="red",
        )
    else:
        info_label.configure(text="Done", text_color="green")
        global last_created_root_path
        last_created_root_path = root_path
    info_window.deiconify()

    # Position the info window relative to the main window
    x = app.winfo_x() + app.winfo_width() // 2 - info_window.winfo_width() // 2
    y = app.winfo_y() + app.winfo_height() // 2 - info_window.winfo_height() // 2
    info_window.geometry(f"+{x}+{y}")


# --- Main Application Window ---
app = ctk.CTk()
app.title("Overmind Studios FolderCreate " + version)
app.geometry("600x400")
app.resizable(False, False)
app.option_add("*Font", "Ubuntu 13")
app.iconbitmap("assets/graphics/appicon.ico")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(3, weight=1)


# --- Preview Window ---
preview_window = ctk.CTkToplevel(app)
preview_window.title("Folder Structure Preview")
preview_window.geometry("500x400")
preview_window.withdraw()  # Hide initially
preview_window.resizable(False, False)

preview_frame = ctk.CTkFrame(preview_window)
preview_frame.pack(expand=True, fill="both", padx=20, pady=20)

preview_textbox = ctk.CTkTextbox(preview_frame, wrap="none")
preview_textbox.pack(expand=True, fill="both", pady=10)

preview_ok_button = ctk.CTkButton(
    preview_frame, text="OK", command=close_preview_window
)
preview_ok_button.pack(pady=10)


def format_paths_as_tree(paths, root_dir):
    """
    Formats a flat list of paths into a human-readable tree structure string.
    """
    if not paths:
        return "(No folders to create)"

    # Build a nested dictionary representation of the tree
    tree = {}
    for path in paths:
        parts = path.split(os.sep)
        current_level = tree
        for part in parts:
            current_level = current_level.setdefault(part, {})

    def build_tree_string(node, indent="", is_last=False, prefix=""):
        s = ""
        keys = list(node.keys())
        for i, key in enumerate(keys):
            is_last_child = i == len(keys) - 1
            s += f"{indent}{prefix}{'└── ' if is_last_child else '├── '}{key}/\n"
            s += build_tree_string(
                node[key],
                indent + ("    " if is_last_child else "│   "),
                is_last_child,
                "",
            )
        return s

    # Start building the string with the root directory
    tree_string = f"{root_dir}/\n"
    tree_string += build_tree_string(tree)
    return tree_string


def show_preview_window():
    # Placeholder for preview generation logic
    preview_textbox.delete("1.0", ctk.END)
    preview_textbox.insert("1.0", "Generating preview...")

    root_path = root_path_entry.get()
    template_name = template_combobox.get()
    template_file_path = os.path.join(TEMPLATE_PATH, template_name)

    try:
        with open(template_file_path, "r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except (FileNotFoundError, yaml.YAMLError, Exception) as e:
        preview_textbox.delete("1.0", ctk.END)
        preview_textbox.insert("1.0", f"Error loading template: {e}")
        preview_window.deiconify()
        return

    if data is None:
        preview_textbox.delete("1.0", ctk.END)
        preview_textbox.insert("1.0", "Template file is empty.")
        preview_window.deiconify()
        return

    paths_to_create = _generate_paths_from_template_data(data)

    if not paths_to_create:
        preview_textbox.delete("1.0", ctk.END)
        preview_textbox.insert(
            "1.0", "Template is valid, but contains no folders to create."
        )
        preview_window.deiconify()
        return

    # Format paths as tree
    tree_string = format_paths_as_tree(paths_to_create, root_path)
    preview_textbox.delete("1.0", ctk.END)
    preview_textbox.insert("1.0", tree_string)

    preview_window.deiconify()
    # Position the preview window relative to the main window
    x = app.winfo_x() + app.winfo_width() // 2 - preview_window.winfo_width() // 2
    y = app.winfo_y() + app.winfo_height() // 2 - preview_window.winfo_height() // 2
    preview_window.geometry(f"+{x}+{y}")



# --- UI Elements ---


# Directory Selection Frame
directory_frame = ctk.CTkFrame(app)
directory_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
directory_frame.grid_columnconfigure(0, weight=1)

root_path_entry = ctk.CTkEntry(
    directory_frame, width=400, placeholder_text="Select Directory"
)
root_path_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

choose_dir_button = ctk.CTkButton(
    directory_frame, text="Browse", command=choose_directory
)
choose_dir_button.grid(row=0, column=1, padx=(0, 0), pady=10)

set_default_path_button = ctk.CTkButton(
    directory_frame, text="Set Default", command=set_default_path
)
set_default_path_button.grid(row=0, column=2, padx=(10, 0), pady=10)

# Initialize root_path_entry with the loaded default path
root_path_entry.insert(0, load_default_path())

# Template Selection Combobox
template_label = ctk.CTkLabel(app, text="Select Template:")
template_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

template_combobox = ctk.CTkComboBox(app, state="readonly")
template_combobox.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

preview_button = ctk.CTkButton(
    app,
    text="Preview Structure",
    command=show_preview_window,
    height=30,
    font=("Ubuntu", 13),
    fg_color=("gray50", "gray30"),  # Less prominent foreground color
    hover_color=("gray40", "gray20"),  # Less prominent hover color
)
preview_button.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="ew")

# Create Folders Button
create_folders_button = ctk.CTkButton(
    app,
    text="Create Folders",
    command=create_folders,
    height=40,
    font=("Ubuntu", 16, "bold"),
)
create_folders_button.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")


# --- Copyright and Version Labels ---
copyright_label = ctk.CTkLabel(
    app,
    text="© 2025 Overmind Studios - Kummer, Gerhardt & Kraus GbR",
    font=("Ubuntu", 10),
)
copyright_label.grid(row=5, column=0, pady=(10, 5))

version_label = ctk.CTkLabel(app, text="version " + version, font=("Ubuntu", 10))
version_label.grid(row=6, column=0, pady=(0, 20))


# --- Info Message Popup Window ---
info_window = ctk.CTkToplevel(app)
info_window.title("Info")
info_window.geometry("300x150")
info_window.withdraw()  # Hide initially

info_frame = ctk.CTkFrame(info_window)
info_frame.pack(expand=True, fill="both", padx=20, pady=20)

info_label = ctk.CTkLabel(info_frame, text="", wraplength=260)
info_label.pack(expand=True, fill="both", pady=10)

ok_button = ctk.CTkButton(info_frame, text="OK", command=close_info_window)
ok_button.pack(pady=10)


# --- Application Initialization ---
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # --- Load Templates and Update UI ---
    templates = load_templates(TEMPLATE_PATH)
    if templates:
        template_combobox.configure(values=templates)
        template_combobox.set(templates[0])
    else:
        template_combobox.set("No templates found")
        template_combobox.configure(state="disabled")
        create_folders_button.configure(state="disabled")

    app.mainloop()
