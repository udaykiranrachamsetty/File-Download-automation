import os
import logging
from os.path import splitext, exists, join
from shutil import move
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

src_directory = r"C:\Users\racha\Downloads"
dest_dir_sfx = r"C:\Users\racha\Downloads\SFX"
dest_dir_music = r"C:\Users\racha\Downloads\Music"
dest_dir_video = r"C:\Users\racha\Downloads\Videos"
dest_dir_image = r"C:\Users\racha\Downloads\Images"
dest_dir_documents = r"C:\Users\racha\Downloads\Documents"

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf",
                    ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd", ".mkv"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]



def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name


# Function to move file to the designated directory
def move_file(dest, entry_path, name):
    if exists(join(dest, name)):
        name = make_unique(dest, name)
    move(entry_path, join(dest, name))


# Handler class for file system events
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(src_directory) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue
                name = entry.name
                dest = None
                if any(name.lower().endswith(ext) for ext in audio_extensions):
                    dest = dest_dir_sfx if "SFX" in name.upper() or entry.stat().st_size < 10_000_000 else dest_dir_music
                elif any(name.lower().endswith(ext) for ext in video_extensions):
                    dest = dest_dir_video
                elif any(name.lower().endswith(ext) for ext in image_extensions):
                    dest = dest_dir_image
                elif any(name.lower().endswith(ext) for ext in document_extensions):
                    dest = dest_dir_documents

                if dest:
                    move_file(dest, entry.path, name)
                    logging.info(f"Moved {name} to {dest}")


if __name__ == "__main__":
    for directory in [dest_dir_music, dest_dir_video, dest_dir_image, dest_dir_documents, dest_dir_sfx]:
        ensure_dir_exists(directory)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, src_directory, recursive=False)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
