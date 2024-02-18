import os
import logging
from os.path import splitext, exists, join
from shutil import move
from time import sleep, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
src_directory = r"C:\Users\racha\Downloads"
dest_directories = {
    'SFX': r"C:\Users\racha\Downloads\SFX",
    'Music': r"C:\Users\racha\Downloads\Music",
    'Videos': r"C:\Users\racha\Downloads\Videos",
    'Images': r"C:\Users\racha\Downloads\Images",
    'Documents': r"C:\Users\racha\Downloads\Documents",
}

file_extension_mappings = {
    ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.psd', '.bmp', '.heif', '.svg', '.ico'): 'Images',
    ('.webm', '.mpg', '.mpeg', '.mp4', '.avi', '.wmv', '.mov', '.mkv'): 'Videos',
    ('.m4a', '.flac', '.mp3', '.wav', '.wma', '.aac'): 'Music',
    ('.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'): 'Documents',
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


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    unique_name = name
    while exists(join(dest, unique_name)):
        unique_name = f"{filename}_{counter}{extension}"
        counter += 1
    return unique_name


def move_file(dest, entry_path, name):
    try:
        unique_name = make_unique(dest, name)
        move(entry_path, join(dest, unique_name))
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
