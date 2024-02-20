import os
import logging
from os.path import exists, join
from shutil import move
from time import sleep, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes  # For pop-up message

# Configuration
src_directory = r"C:\Users\racha\Downloads"
dest_directories = {
    'SFX': r"C:\Users\racha\Downloads\SFX",
    'Music': r"C:\Users\racha\Downloads\Music",
    'Videos': r"C:\Users\racha\Downloads\Videos",
    'Images': r"C:\Users\racha\Downloads\Images",
    'Documents': r"C:\Users\racha\Downloads\Documents",
    'Archives': r"C:\Users\racha\Downloads\Archives",
}

file_extension_mappings = {
    ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.psd', '.bmp', '.heif', '.svg', '.ico'): 'Images',
    ('.webm', '.mpg', '.mpeg', '.mp4', '.avi', '.wmv', '.mov', '.mkv'): 'Videos',
    ('.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac', '.ogg', '.opus'): 'Music',
    ('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'): 'Documents',
    ('.zip', '.rar', '.7z', '.tar', '.gz'): 'Archives',
}

# Debounce settings
last_processed_time = time()
debounce_delay = 2  # seconds

def ensure_dir_exists():
    for directory in dest_directories.values():
        if not exists(directory):
            os.makedirs(directory)

def find_destination_extension(file_name):
    for extensions, category in file_extension_mappings.items():
        if any(file_name.lower().endswith(ext) for ext in extensions):
            return dest_directories[category]
    return None

def move_file(dest, entry_path, name):
    destination_path = join(dest, name)
    if exists(destination_path):
        logging.info(f"File {name} already exists in {dest}.")
        ctypes.windll.user32.MessageBoxW(0, f"File {name} already exists in {dest}.", "File Exists", 1)
    else:
        try:
            move(entry_path, destination_path)
            logging.info(f"Moved {name} to {dest}")
        except Exception as e:
            logging.error(f"Error moving {name} to {dest}: {e}")

class MoverHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global last_processed_time
        current_time = time()
        if current_time - last_processed_time > debounce_delay:
            self.process_directory()
            last_processed_time = current_time

    def process_directory(self):
        for root, dirs, files in os.walk(src_directory):
            for name in files:
                full_path = join(root, name)
                dest = find_destination_extension(name)
                if dest:
                    move_file(dest, full_path, name)

if __name__ == "__main__":
    ensure_dir_exists()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, src_directory, recursive=True)
    observer.start()

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
