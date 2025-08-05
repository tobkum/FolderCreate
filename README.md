# FolderCreate

FolderCreate is a simple desktop application that creates a folder structure based on predefined YAML templates. It provides a user-friendly graphical interface to select a root directory and a template, and then generates the specified directory tree.

## Features

*   **Graphical User Interface (GUI):** An intuitive interface for selecting directories and templates.
*   **Template-Based:** Uses easy-to-edit YAML files to define complex folder structures.
*   **Customizable Templates:** Users can create their own YAML templates for different project types.
*   **Error Handling:** Provides feedback on errors, such as missing templates or parsing issues.

## Usage

1.  Launch the application.
2.  Click the **Browse** button to select the root directory where you want to create the new folders.
3.  Select a template from the dropdown menu.
4.  Click the **Create Folders** button.
5.  The application will create the folder structure defined in the selected template within the chosen root directory.

## Templates

The folder structures are defined in `.yaml` files located in the `templates` directory. The application automatically loads all `.yaml` or `.yml` files from this directory.

### Template Format

The YAML templates use a simple nested list and dictionary format to represent the folder hierarchy.

**Example (`01-VFX.yaml`):**

```yaml
- 00-BRIEFING
- 01-FROM_CLIENT
- 10-OWN_FOOTAGE:
  - 00-RENDER
  - 10-IMAGES
- 50-WORKSPACE:
  - 00-DEFAULT:
    - 10-BLENDER
    - 20-FUSION
- 99-DELIVERIES
```

This template will create a folder structure like this:

```
<root_directory>/
├── 00-BRIEFING/
├── 01-FROM_CLIENT/
├── 10-OWN_FOOTAGE/
│   ├── 00-RENDER/
│   └── 10-IMAGES/
├── 50-WORKSPACE/
│   └── 00-DEFAULT/
│       ├── 10-BLENDER/
│       └── 20-FUSION/
└── 99-DELIVERIES/
```

### Creating New Templates

1.  Create a new `.yaml` file in the `templates` directory.
2.  Define your desired folder structure using the format described above.
3.  The new template will be available in the dropdown menu the next time you run the application.

## Dependencies

This application requires the following Python libraries:

*   **customtkinter**
*   **PyYAML**

You can install them using pip from the `Pipfile`:

```bash
pip install -r Pipfile
```

## License

This project is licensed under the terms of the LICENSE file.

---
*© 2025 Overmind Studios - Kummer, Gerhardt & Kraus GbR*
