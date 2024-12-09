from colorama import Fore
import argparse
from aiofiles.ospath import isdir
from aiofiles.os import makedirs, scandir
import aiofiles
import asyncio
import os

async def init_path(source_dir: str, target_dir: str):
    # Асинхронно перевіряє та ініціалізує шляхи для вихідної та цільової директорій.
  
    # Перевірка існування вихідної директорії
    if not await isdir(source_dir):
        raise FileNotFoundError(f"Вихідна директорія '{source_dir}' не існує.")

    # Перевірка цільової директорії; створюємо, якщо її немає
    if not await isdir(target_dir):
        print(f"Цільова директорія '{target_dir}' не існує. Створюємо...")
        await makedirs(target_dir, exist_ok=True)

    return source_dir, target_dir

def pars_args():
    # Парсинг аргументів командного рядка

    parser = argparse.ArgumentParser(description="Ініціалізація шляхів для вихідної та цільової директорій.")

    parser.add_argument("--source", required=True, help="Шлях до вихідної директорії.")
    parser.add_argument("--target", required=True, help="Шлях до цільової директорії.")

    return parser.parse_args()

async def read_folder(source_dir, target_dir):
    # Асинхронно читає вміст папки, рекурсивно обробляючи всі вкладені файли та директорії.

    for el in os.scandir(source_dir):
        if el.is_dir():
            print(f'Опрацьовую директорію: {el}')
            await read_folder(el.path, target_dir)
        else:
            await copy_file(el.path, target_dir)

async def copy_file(source_file, target_dir):
    # Асинхронно копіює файл у відповідну підпапку в цільовій директорії на основі розширення файлу.

    # Отримуємо розширення файлу
    _, extension = os.path.splitext(source_file)
    extension = extension.lstrip('.').lower()

    if not extension:
        extension = 'unknown'

    # Створюємо цільову папку для розширення
    target_subdir = os.path.join(target_dir, extension)
    os.makedirs(target_subdir, exist_ok=True)

    # Формуємо шлях до цільового файлу
    target_file = os.path.join(target_subdir, os.path.basename(source_file))

    # Асинхронне копіювання файлу
    async with aiofiles.open(source_file, mode='rb') as src, aiofiles.open(target_file, mode='wb') as dst:
        while chunk := await src.read(1024*1024): 
            await dst.write(chunk)
    print(f"Файл {source_file} скопійовано в {target_file}")

async def main():
    args = pars_args()

    try:
        source_path, target_path = await init_path(args.source, args.target)
        await read_folder(source_path, target_path)
        print(Fore.BLUE + f"Вихідна директорія: {source_path}")
        print(Fore.GREEN + f"Цільова директорія: {target_path}")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
