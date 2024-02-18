# File Organizer

## Description

This project includes a Python script designed to automatically organize files in the `Downloads` directory into categorized folders based on their file type. It supports various file types including images, videos, audio files, and documents. The script utilizes the `watchdog` library for real-time monitoring of the directory, sorting new files as they are downloaded.

## Features

- **Real-time Monitoring**: Automatically detects new files in the `Downloads` directory.
- **Automatic Organization**: Sorts files into designated folders based on file extension.
- **Support for Various File Types**: Predefined categories for images, videos, audio, and documents.
- **Extensible**: Easily add more file types and categories.

## Prerequisites

- Python 3.6 or later.
- `watchdog` Python library.

## Installation

### Clone the Repository

1. Clone the project to your local machine and navigate into the project directory:

```bash
git clone https://github.com/udaykiranrachamsetty/File-Organizer.git
cd File-Organizer

```
## Convert Script to Executable (Optional)
For Windows users who wish to run the script at startup:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```
After conversion, the executable will be located in the dist directory. You can directly use this executable without running the script through a Python interpreter.

## Using the Executable
Navigate to the dist folder to find the executable version of your script:
```bash
File-Organizer/dist/main.exe
To set the script to run at startup, copy main.exe to your Startup folder (accessible by typing shell:startup in the Run dialog on Windows).
```
## Usage

**Direct Execution**: Run python main.py from the command line if not using the executable.\n
**Executable**: Double-click main.exe in the dist folder or place it in your startup folder for automatic execution on system startup.



