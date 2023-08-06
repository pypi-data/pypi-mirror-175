from os import walk
import json
import os
import tablib



def get_env_file_path() -> str | None:
    path = f"{get_current_working_directory()}/.env"

    return path


def get_virtual_env_path() -> str | None:
    path = os.environ['VIRTUAL_ENV']

    return path


def get_current_working_directory() -> str | None:
    path = os.getcwd()

    return path


def get_all_files(path: str, filter_extension=".json") -> list[str]:
    files = []

    for (_dirpath, _dirnames, filenames) in walk(path):
        for file_name in filenames:
            path, ext = os.path.splitext(file_name)
            if not filter_extension or ext == filter_extension:
                files.append(file_name)
        break

    return files


def read_json_file(fullpath, quiet=False) -> any:
    if not quiet:
        print("Reading json file: ", fullpath)
    with open(fullpath) as file:
        datastr = file.read()

    data = json.loads(datastr)  # simple check if action is valid json

    return data


def read_file(fullpath: str, quiet=False) -> bytes:
    if not quiet:
        print("Reading file", fullpath)

    with open(fullpath, "rb") as file:
        datastr = file.read()

    return datastr


def write_json(data: dict, filename: str):
    with open(filename, "wb") as file:
        file.write(json.dumps(data, indent=2, ensure_ascii=False).encode())


def write_excel(tablib_data: list, filename: str, verbose: bool):
    dataset = tablib.Dataset(*tablib_data)

    if verbose:
        print('Writing to', filename)

    with open(filename, "wb") as file:
        file.write(dataset.export('xlsx'))
