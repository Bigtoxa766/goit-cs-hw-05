from colorama import Fore
import asyncio
import argparse

from aiopath import AsyncPath
import os
import sys

# Створення об'єкта ArgumentParser
parser = argparse.ArgumentParser(description="Програма для обробки аргументів командного рядка.")

# Додавання аргументів
parser.add_argument(
    '--source',
    required=True,
    help="Вихідна директорія (обов'язковий аргумент)"
)

parser.add_argument(
    '--output',
    required=True,
    help="Директорія призначення (обов'язковий аргумент)"
)

# Обробка аргументів
args = parser.parse_args()


# if len(sys.argv) > 1:
#     directory_path = sys.argv[1]
# else:
#     directory_path = input("Enter directory path: ")

# if not os.path.isdir(directory_path):
#     print(f"{directory_path} file or directory not exist.")
#     sys.exit(1)

# def parse_dir(path):
#     for el in path.iterdir():
#         if el.is_dir():
#             parse_dir(el)
#             print(Fore.BLUE + f'This is folder: {el}')
#         else:
#             print(Fore.GREEN + f'This is file: {el}')

# core_path = Path(directory_path)
# parse_dir(core_path)