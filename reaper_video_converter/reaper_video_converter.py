import os
import subprocess
import sys
from pathlib import Path
from shutil import which

import puremagic
import yamale
from loguru import logger
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.parser import ParserError

# Get application path
if getattr(sys, 'frozen', False):
    # noinspection PyUnresolvedReferences, PyProtectedMember
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# Declare YAML config schema
schema = yamale.make_schema(content="""
video:
    video_codec: enum("prores", "mjpeg")
audio:
    enable_audio: bool()
    audio_codec: enum("pcm_s16le", "pcm_s24le", "pcm_f32le", "copy", required=False, none=False)
    audio_samplerate: enum(44100, 48000, 96000, 192000, 0, required=False, none=False)
""", parser="ruamel")

# Check config path and validate it
config_path = Path("reaper_video_converter.yaml").resolve()
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
video_codec: str = config.get("video").get("video_codec")
enable_audio: bool = config.get("audio").get("enable_audio")
audio_codec: str = config.get("audio").get("audio_codec", "copy")
audio_samplerate: int = config.get("audio").get("audio_samplerate", 0)

# Check if exists in PATH or in the same folder as the application
if (Path(application_path).resolve() / "ffmpeg.exe").is_file():
    ffmpeg_path = Path(application_path).resolve() / "ffmpeg.exe"
    logger.info("FFmpeg executable found! 👍")
elif (Path(application_path).resolve() / "ffmpeg").is_file():
    ffmpeg_path = Path(application_path).resolve() / "ffmpeg"
    logger.info("FFmpeg executable found! 👍")
elif which("ffmpeg.exe"):
    ffmpeg_path = Path(which("ffmpeg.exe")).resolve()
    logger.info("FFmpeg executable found! 👍")
elif which("ffmpeg"):
    ffmpeg_path = Path(which("ffmpeg")).resolve()
    logger.info("FFmpeg executable found! 👍")
else:
    logger.error("Can't find the FFmpeg executable. 😭")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Check if FFmpeg is runnable
if not os.access(ffmpeg_path, os.X_OK):
    logger.error("Not enough permissions to run FFmpeg. 😭")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Get arguments, check if the number of arguments is correct and get input file path
args = sys.argv
if len(args) != 2:
    logger.error("Number of arguments is incorrect. 😭")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)
input_file: Path = Path(args[1]).resolve()

# Check if input file is a file
if input_file.is_file():
    logger.info("Input file found! 👍")
else:
    logger.error(f"Input file is not a file or doesn't exist. 😭\n{input_file}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Check if input file is a video
try:
    input_file_is_video = "video" in puremagic.from_file(str(input_file), mime=True)
    if not input_file_is_video:
        logger.warning("Input file may not be a video, other errors are possible.")
except puremagic.main.PureError:
    logger.warning("Couldn't check input file MIME type, other errors are possible.")

# Generate output file path and check if it exists
output_file: Path = input_file.parent / (input_file.stem + "_" + video_codec.upper() + input_file.suffix)
if output_file.is_file():
    logger.error("Output file exists! Please move it, delete it, or use another video codec. 😭")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)

# Generate args for subprocess
subprocess_args = [str(ffmpeg_path), "-n", "-hide_banner",
                   "-i", str(input_file),
                   "-c:v", video_codec,
                   "" if enable_audio else "-an",
                   "-c:a", audio_codec,
                   "-ar", str(audio_samplerate),
                   str(output_file)]
subprocess_args.remove("")


# Define run_command function that allows us to see realtime output of the subprocess
def run_command(command) -> int:
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


# Run FFmpeg
try:
    logger.info("Here goes the FFmpeg output! ⬇️️️")
    exit_code = run_command(subprocess_args)
    input("\nPress Enter to close...\n\n")
    sys.exit(exit_code)
except PermissionError as e:
    logger.error(f"Not enough permissions to run FFmpeg. 😭\n{e}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)
except OSError as e:
    logger.error(f"Something went wrong with running FFmpeg. 😭\n{e}")
    input("\nPress Enter to exit...\n\n")
    sys.exit(1)
