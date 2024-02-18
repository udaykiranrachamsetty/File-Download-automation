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

Clone the project to your local machine and navigate into the project directory:

```bash
git clone https://github.com/udaykiranrachamsetty/File-Organizer.git
cd File-Organizer


## Convert Script to Executable (Optional)
For Windows users who wish to run the script at startup:

```bash
pip install pyinstaller
pyinstaller --onefile main.py

