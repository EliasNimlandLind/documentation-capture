# Documentation Capture

## About

The scripts are made to assist in the creation documentation, by capturing screenshots of the current window only, on each mouse key press. The screenshots are altered to highlight the mouse's position and adding a space at the bottom of the image used to add additional text.

## Keybindings and configuration

|        Key        |       Action       |
| :---------------: | :----------------: |
|      Escape       | Termintes program  |
| Left mouse button | Capture screenshot |

Change configuration values in _config.ini_.

## Setup and execution

## Setup and installing

Settings can be changed in _config.ini_.

1. Install dependencies.

### Using the Python command line interface

2. Execute `python __init__.py`.

### Using .exe files

3. Execute `cd <root directory>`-
4. Execute `pyinstaller --onefile src\documentation-capture\__init__.py`-
5. Create an installer using _installer-script.iss_ and Inno Setup Compiler.
6. Execute installer wizard.
7. Execute _documentation-capture-application.exe_ inside the directory created during installation.
