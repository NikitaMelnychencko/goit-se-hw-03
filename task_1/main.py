import argparse
from pathlib import Path
import shutil
import logging
from threading import Thread

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", '--s',  help="Source folder", required=True)
parser.add_argument("--output", '--o',  help="Output folder", default="dist")
args = vars(parser.parse_args())
print(args)
source = Path(args["source"])
output = Path(args["output"])
folders= []

def get_folder(path):
    for item in path.iterdir():
        if item.is_dir():
            folders.append(item)
            get_folder(item)

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
  folders.append(source)
  get_folder(source)
  threads = []
  for folder in folders:
    thread = Thread(target=copy_file, args=(folder,))
    thread.start()
    threads.append(thread)
  for thread in threads:
    thread.join()
  logging.info("All files copied")