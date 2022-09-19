from yaml import safe_load
from os import getcwd, path, makedirs
from sys import argv

template_path = path.join(getcwd(), "templates")
root_path = ""
template_file = ""

newpaths = []


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


def folder_create():
    if len(argv) == 3:
        template_file = argv[1]
        root_path = argv[2]
    else:
        print("Invalid number of arguments, please pass the template name and the root path")
        print("Example: python FolderCreate.py VFX.yaml d:\\projects\\projectname")
        quit()

    with open(path.join(template_path, template_file), 'r') as stream:
        data = safe_load(stream)
        dict_to_dir(data)

    for i in newpaths:
        print(path.join(root_path, i))
        makedirs(path.join(root_path, i))


if __name__ == "__main__":
    folder_create()
