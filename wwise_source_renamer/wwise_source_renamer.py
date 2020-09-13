import os
import sys
import time
from pathlib import Path

import yamale
from P4 import P4, P4Exception
from loguru import logger
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.parser import ParserError
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Get application path
if getattr(sys, 'frozen', False):
    # noinspection PyUnresolvedReferences, PyProtectedMember
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Declare YAML config schema
schema = yamale.make_schema(content="""
options:
    wwise_project_path: str()
    rename_sound_object: bool()
perforce:
    port: str()
    user: str()
    client: str()
""", parser="ruamel")

# Check config path and validate it
config_path = Path("wwise_source_renamer.yaml").resolve()
if config_path.is_file():
    logger.info("Config found! 👍")
    try:
        data = yamale.make_data(config_path, parser="ruamel")
        yamale.validate(schema, data)
        logger.info("Config validation success! 👍")
    except (ParserError, YAMLError) as e:
        logger.error(f"Something wrong with the config file (either not YAML or invalid YAML). 😭\n{str(e)}")
        input("\nPress Enter to exit...\n\n")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Config validation failed. 😭\n{str(e)}")
        input("\nPress Enter to exit...\n\n")
        sys.exit(1)
else:
    logger.error(f"Config file is not a file or doesn't exist. 😭\n{config_path}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Open config
yaml = YAML()
try:
    config = yaml.load(config_path)
    logger.info(f"Config successfully loaded! 👍")
except (ValueError, ParserError, YAMLError) as e:
    logger.error(f"Something wrong with reading the config file. 😭\n{str(e)}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Get config values
wwise_project_path: str = config.get("options").get("wwise_project_path")
rename_sound_object: bool = config.get("options").get("rename_sound_object")
p4_host: str = config.get("perforce").get("host")
p4_port: int = config.get("perforce").get("port")
p4_user: str = config.get("perforce").get("user")
p4_client: str = config.get("perforce").get("client")


class WwiseSourceRenamer:
    def __init__(self, project_path, rename_sound_object_bool):
        self._project_path = project_path
        self._changed_files: list = []
        self._changed_files_validated: list = []
        self._rename_sound_object: bool = rename_sound_object_bool

        self.validate_wwise_project()

    def validate_wwise_project(self):
        print(f"Validate Wwise project: {self._project_path}")

    def rename_wwise_source(self, src_path, dest_path):
        self._changed_files.append(dest_path)
        # TODO: Write implementation
        print(f"Rename {src_path} to {dest_path} in Wwise project files.")

    def get_changed_files(self):
        for file in self._changed_files:
            if (file_path := Path(file).resolve()).is_file():
                self._changed_files_validated.append(file_path)
        return self._changed_files_validated


class OnMovedEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        super(OnMovedEventHandler, self).on_moved(event)
        if not event.is_directory:
            logger.info(f"Moved file: from {event.src_path} to {event.dest_path}")
            renamer.rename_wwise_source(event.src_path, event.dest_path)


renamer = WwiseSourceRenamer(wwise_project_path, rename_sound_object)

observer = Observer()
observer.schedule(OnMovedEventHandler(), wwise_project_path, recursive=True)
observer.start()
logger.info(f"Started watching this directory: {wwise_project_path}")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

# P4 initialization and credentials
p4 = P4()
p4.port = str(p4_port)
p4.user = p4_user
p4.client = p4_client

# TODO: Remove
exit(0)

# Connect to P4
try:
    logger.info("Trying to connect to P4. May take some time.")
    p4.connect()
except P4Exception as e:
    logger.error(f"Unable to connect to P4. 😭\n{e}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Disconnect from P4
try:
    p4.disconnect()
except P4Exception as e:
    logger.error(f"Unable to disconnect from P4. 😭\n{e}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)
