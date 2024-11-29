"""
Відсортувати файли в папці.
"""

import argparse
import sys
from pathlib import Path
from shutil import copyfile
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import logging

"""
--source [-s] 
--output [-o] default folder = dist
"""

logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

# Аргументи командного рядка
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

# Пул потоків для копіювання файлів
copy_pool = ThreadPoolExecutor(max_workers=8)


def reader_folder(path: Path) -> None:
    """Рекурсивний обхід директорій."""
    logging.info(f"Processing folder: {path}")
    folders = []

    for el in path.iterdir():
        if el.is_dir():
            # Обробка підкаталогів у нових потоках
            inner_thread = Thread(target=reader_folder, args=(el,))
            folders.append(inner_thread)
            inner_thread.start()
        else:
            # Додавання завдань копіювання до пулу потоків
            copy_pool.submit(copy_file, el)

    # Чекаємо завершення потоків для підкаталогів
    for folder in folders:
        folder.join()


def copy_file(path: Path) -> None:
    """Копіювання файлу у відповідну папку за розширенням."""
    ext = path.suffix[1:]  # Розширення файлу без точки
    ext_folder = output / ext
    try:
        ext_folder.mkdir(exist_ok=True, parents=True)  # Створення папки для розширення
        copyfile(path, ext_folder / path.name)
        logging.info(f"Copied: {path} to {ext_folder}")
    except OSError as err:
        logging.error(f"Error copying {path}: {err}")


if __name__ == "__main__":
    # Перевірка існування вихідної папки
    if not source.exists() or not source.is_dir():
        logging.error(f"Source folder does not exist or is not a directory: {source}")
        sys.exit(1)

    # Старт рекурсивної обробки
    logging.info(f"Starting to process: {source}")
    reader_folder(source)
    copy_pool.shutdown(wait=True)  # Закриття пулу потоків після завершення роботи
    logging.info(f"Processing complete. Sorted files are in: {output}")
    print(f"You can delete {source}")

# MainThread Starting to process: picture
# MainThread Processing folder: picture
# Thread-1 (reader_folder) Processing folder: picture\icons
# Thread-2 (reader_folder) Processing folder: picture\Logo
# Thread-3 (reader_folder) Processing folder: picture\Other
# Thread-4 (reader_folder) Processing folder: picture\wallpaper
# ThreadPoolExecutor-0_0 Copied: picture\bot-icon.png to dist\png
# ThreadPoolExecutor-0_1 Copied: picture\javascript_encapsulation.jpg to dist\jpg
# ThreadPoolExecutor-0_3 Copied: picture\icons\mongodb.jpg to dist\jpg
# Thread-5 (reader_folder) Processing folder: picture\Other\Icons
# ThreadPoolExecutor-0_2 Copied: picture\icons\e-learning_icon.jpg to dist\jpg
# ThreadPoolExecutor-0_4 Copied: picture\Logo\IBM+Logo.png to dist\png
# ThreadPoolExecutor-0_0 Copied: picture\Other\golang.png to dist\png
# ThreadPoolExecutor-0_5 Copied: picture\Logo\ibm.svg to dist\svg
# ThreadPoolExecutor-0_1 Copied: picture\wallpaper\js.png to dist\png
# ThreadPoolExecutor-0_7 Copied: picture\Logo\logo-tm.png to dist\png
# ThreadPoolExecutor-0_6 Copied: picture\Other\hqdefault.jpg to dist\jpg
# ThreadPoolExecutor-0_3 Copied: picture\wallpaper\node-wallpaper.jpg to dist\jpg
# ThreadPoolExecutor-0_4 Copied: picture\Other\Icons\1600.png to dist\png
# ThreadPoolExecutor-0_2 Copied: picture\Other\nodejslogo.png to dist\png
# MainThread Processing complete. Sorted files are in: dist