import argparse
from pathlib import Path
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor
import threading


parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", '--s',  help="Source folder", required=True)
parser.add_argument("--output", '--o',  help="Output folder", default="dist")
args = vars(parser.parse_args())
print(args)
source = Path(args["source"])
output = Path(args["output"])
lock = threading.RLock()
folders= []
tasks = []

def get_folder(path):
    for item in path.iterdir():
        if item.is_dir():
            with lock:
                folders.append(item)
                tasks.append(executor.submit(get_folder, item))

def copy_file(path):
    for item in path.iterdir():
        if item.is_file():
            extension = item.suffix[1:]
            new_path = Path(args["output"]) / extension
            try:
                new_path.mkdir(parents=True, exist_ok=True)
            except OSError:
                print(f"Error creating directory: {new_path}")
                continue
            shutil.copy(item, new_path)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
  with ThreadPoolExecutor(max_workers=20) as executor:
    tasks.append(executor.submit(get_folder, source))
    index = 0
    while index < len(tasks):
        tasks[index].result()
        index += 1

  with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(copy_file, folders)
  logging.info("All files copied")