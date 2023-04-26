import dearpygui.dearpygui as dpg
from yaml import safe_load

from os import path, getcwd, listdir, makedirs

templates = []
newpaths = []

default_path = "X:/Geteilte Ablagen/"
template_path = template_path = path.join(getcwd(), "templates")
for file in listdir(template_path):
    if file.endswith(".yaml"):
        templates.append(file)


def dict_to_dir(data, top_path=""):
    if isinstance(data, dict):
        for k, v in data.items():
            dict_to_dir(v, k)
    elif isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                for k, v in i.items():
                    dict_to_dir(v, path.join(top_path, k))
            else:
                newpaths.append(path.join(top_path, i))


dpg.create_context()


def callback(_sender, app_data):
    dpg.set_value(path_text, app_data["current_path"])


def cancel_callback(_sender, _app_data):
    pass


def create_folders():
    template = dpg.get_value("chosen_template")
    root_path = dpg.get_value("root_path")
    with open(path.join(template_path, template), 'r') as stream:
        data = safe_load(stream)
        dict_to_dir(data)
    for i in newpaths:
        try:
            makedirs(path.join(root_path, i))
        except Exception:
            print('An error occured, please check if the directory is writable.')
    dpg.configure_item("modal_id", show=True)
    dpg.configure_item("message", default_value="Done")


with dpg.window(tag="Primary Window"):
    with dpg.group(horizontal=True) as directory_group:
        path_text = dpg.add_input_text(default_value=default_path, tag="root_path")
        dpg.add_button(
            label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id")
        )
        dpg.add_file_dialog(
            directory_selector=True,
            show=False,
            callback=callback,
            tag="file_dialog_id",
            cancel_callback=cancel_callback,
            width=600,
            height=500,
            default_path=default_path,
        )

    dpg.add_combo(label="Select Template", items=templates, default_value=templates[0], tag="chosen_template")

    dpg.add_button(
        label="Create Folders", callback=create_folders, width=-1, height=50
    )
    dpg.add_text("version 0.1")
    dpg.add_text("© 2023 Overmind Studios")

    with dpg.window(
        label="Info",
        modal=True,
        show=False,
        tag="modal_id",
        pos=(300, 200),
        width=200,
        no_resize=True
    ):
        dpg.add_text("ERROR", tag="message")
        dpg.add_button(
            label="OK",
            callback=lambda: dpg.configure_item("modal_id", show=False),
            width=-1
        )


dpg.create_viewport(
    title="Overmind Studios Folder Create", width=700, height=600, decorated=True
)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
