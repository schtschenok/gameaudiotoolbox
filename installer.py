import logging
import os
import subprocess
import sys
import urllib.request
from distutils.version import StrictVersion
from pathlib import Path
from typing import Sequence
from zipfile import ZipFile, BadZipFile

logging.basicConfig(level=logging.INFO)


class Error(Exception):
    pass


def install_python(python_version: str, pip_packages: Sequence[str]) -> Path:
    common_exceptions = (NameError, ValueError, OSError, PermissionError, IOError, TypeError)

    logging.info("Generating URLs")
    try:
        python_version_strict = str(StrictVersion(python_version))
    except common_exceptions:
        raise Error("Please provide valid Python version")

    if python_version_strict < StrictVersion("3.6"):
        raise Error("Python version should be higher than 3.6")

    python_version_short = "".join(python_version.split(".")[:2])

    python_zip_url = "https://www.python.org/ftp/python/" + \
                     python_version + \
                     "/python-" + \
                     python_version + \
                     "-embed-amd64.zip"
    python_zip_path = Path("./python-" + python_version + "-embed-amd64.zip").resolve()

    python_folder_path = Path("./python-" + python_version).resolve()

    if python_folder_path.is_dir():
        raise Error(f"Folder {python_folder_path} already exists")

    python_exe_path = python_folder_path / "python.exe"

    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = Path("./get-pip.py").resolve()

    pip_path = python_folder_path / "Scripts/pip.exe"

    logging.info("Downloading Python zip archive")
    try:
        with urllib.request.urlopen(python_zip_url) as f:
            python_zip = f.read()
    except common_exceptions:
        raise Error("Something went wrong with downloading Python zip archive")

    logging.info("Writing Python zip archive")
    try:
        with open(python_zip_path, "wb") as f:
            f.write(python_zip)
            f.close()
    except common_exceptions:
        raise Error("Something went wrong with writing Python zip archive")

    logging.info("Unzipping Python")
    try:
        with ZipFile(python_zip_path, "r") as z:
            z.extractall(python_folder_path)
            z.close()
    except (*common_exceptions, BadZipFile):
        raise Error("Something went wrong with unzipping Python zip archive")

    logging.info("Removing Python zip archive")
    try:
        os.remove(python_zip_path)
    except common_exceptions:
        raise Error("Something went wrong with removing Python zip archive")

    logging.info("Changing ._pth")
    try:
        with open(python_folder_path / ("python" + python_version_short + "._pth"), "a") as f:
            f.write("\n# Added by SpawnPython\nimport site\n")
            f.close()
    except common_exceptions:
        raise Error("Something went wrong with writing ._pth")

    logging.info("Changing sitecustomize.py")
    try:
        with open(python_folder_path / "sitecustomize.py", "w") as f:
            f.write("import sys\nsys.path.insert(0, \"\")")
            f.close()
    except common_exceptions:
        raise Error("Something went wrong with writing sitecustomize.py")

    logging.info("Downloading get_pip.py")
    try:
        with urllib.request.urlopen(get_pip_url) as f:
            get_pip_script = f.read()
    except common_exceptions:
        raise Error("Something went wrong with downloading get_pip.py")

    logging.info("Writing get_pip.py")
    try:
        with open(get_pip_path, "wb") as f:
            f.write(get_pip_script)
            f.close()
    except common_exceptions:
        raise Error("Something went wrong with writing get_pip.py")

    logging.info("Running get_pip.py")
    try:
        subprocess.run([python_exe_path, get_pip_path, "--no-warn-script-location"])
    except common_exceptions:
        raise Error("Something went wrong with running get_pip.py")

    logging.info("Removing get_pip.py")
    try:
        os.remove(get_pip_path)
    except common_exceptions:
        raise Error("Something went wrong with removing get_pip.py script")

    logging.info("Installing pip packages")
    try:
        subprocess.run((pip_path, "install", "--no-cache-dir", "-U", "--no-warn-script-location") + tuple(pip_packages))
    except common_exceptions:
        raise Error("Something went wrong with installing pip packages")

    logging.info(f"Python {python_version} is available at {python_exe_path}")
    return python_exe_path


# TODO: Implement
def generate_bat_script(python_script_path: Path, destination_folder: Path) -> Path:
    return Path()


try:
    install_python("3.8.5", ("yamale", "loguru", "p4python", "watchdog", "ruamel.yaml"))
except Error as e:
    logging.error(f"Error occurred\n{e}")
    sys.exit(1)
