import dearpygui.dearpygui as dpg
from dearpygui_ext.themes import create_theme_imgui_dark
from yaml import safe_load
from pathlib import Path

# Initialize variables
version = "0.1"
default_path = "X:/Geteilte Ablagen/"
template_path = Path.cwd() / "templates"
templates = [f.name for f in template_path.glob("*.yaml")]
newpaths = []

# Function to convert dictionary to directory structure
def dict_to_dir(data, top_path=Path()):
    if isinstance(data, dict):
        for k, v in data.items():
            dict_to_dir(v, top_path / k)
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                for k, v in i.items():
                    dict_to_dir(v, top_path / k)
            else:
                newpaths.append(top_path / i)

# DearPyGui context and window setup
dpg.create_context()
with dpg.font_registry():
    default_font = dpg.add_font("assets/fonts/Ubuntu-Regular.ttf", 16)
    dpg.bind_font(default_font)

def create_folders():
    template = dpg.get_value("chosen_template")
    root_path = Path(dpg.get_value("root_path"))
    with open(template_path / template, "r") as stream:
        data = safe_load(stream)
        dict_to_dir(data)
    for i in newpaths:
        try:
            (root_path / i).mkdir(parents=True, exist_ok=True)
        except Exception:
            dpg.set_value("message", "An error occurred, please check if the directory is writable.")
        else:
            dpg.set_value("message", "Done")
    dpg.show_item("modal_id")

# DearPyGui UI setup
with dpg.window(tag="Primary Window", autosize=True):
    dpg.add_input_text(default_value=default_path, tag="root_path")
    dpg.add_button(label="Choose Directory", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_file_dialog(directory_selector=True, show=False, callback=lambda s, a: dpg.set_value("root_path", a["current_path"]),
                        tag="file_dialog_id", cancel_callback=lambda: None, width=600, height=500, default_path=default_path, modal=True)
    dpg.add_combo(label="Select Template", items=templates, default_value=templates[0], tag="chosen_template")
    dpg.add_button(label="Create Folders", callback=create_folders, width=-1, height=50)
    dpg.add_text(f"© 2023 Overmind Studios - Kummer & Gerhardt GbR\nversion {version}")

    with dpg.window(label="Info", modal=True, show=False, tag="modal_id", pos=(300, 200), no_resize=True, autosize=True):
        dpg.add_text("ERROR", tag="message")
        dpg.add_button(label="OK", callback=lambda: dpg.configure_item("modal_id", show=False), width=-1)

dpg.create_viewport(title=f"Overmind Studios FolderCreate {version}", width=700, height=600, decorated=True)
dpg.bind_theme(create_theme_imgui_dark())
dpg.setup_dearpygui()
dpg.set_viewport_large_icon("assets/graphics/appicon.ico")
dpg.set_viewport_small_icon("assets/graphics/appicon.ico")
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()