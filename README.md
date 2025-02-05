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

3. Execute `cd <directory of __init__.py>`-
4. Execute `pyinstaller --onefile __init__.py`-
5. Create an installer using _installer-script.iss_ and Inno Setup Compiler.
6. Execute installed .exe files.
