#!/usr/bin/env python3

"""
Problem: Automatically generate a Minecraft sounds.json file from a folder structure
Target Users: Me
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Take a series of .ogg files and create the JSON manifest.
Allow the user to copy .ogg files to an existing pack and merge JSON files together.
Notes:

In order to get this script to work as a command from any directory, I had to add the following
into my fish.config:
export PYTHONPATH="$PYTHONPATH:{full path to tinytag sub-folder inside venv folder}

Command-line arguments:

    --help      (-h)    Show usage
    --version   (-v)    Show version number
"""

__version__ = '0.16'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"


# Import modules
from collections import OrderedDict
from json_encoder import CompactJSONEncoder
from pathlib import Path
from tinytag import TinyTag
from typing import TypedDict, NotRequired

import argparse
import json
import pathlib
import re
import shutil
import sys


class Sound(TypedDict):
    name: str
    volume: NotRequired[float]
    pitch: NotRequired[float]
    weight: NotRequired[int]
    stream: NotRequired[bool]
    attenuation_distance: NotRequired[int]
    preload: NotRequired[bool]
    type: NotRequired[str]


class SoundEvent(TypedDict):
    replace: bool
    sounds: list[Sound]
    subtitle: str


def handle_command_line():
    """
    Handle arguments supplied by the user
    """

    parser = argparse.ArgumentParser(
        prog="Sound Pack Checker",
        description="generates lists of invalid connections between json and sound files.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __version__)

    parser.add_argument(
        "-s",
        "--source",
        type=Path,
        default=Path.cwd(),
        help="Path to the source folder. Ogg files to be indexed are found here.")

    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        default=type('NonePath', (), {'resolve': lambda: None}),
        help="Path to the target folder. Ogg files will be copied here, if allowed.")

    args = parser.parse_args()

    if src := validate_source(args.source):
        sys.exit(src.format("source"))

    if tgt := validate_target(args.target):
        sys.exit(tgt.format("target"))

    # print(f"args: {args}"); sys.exit()
    return args


def validate_source(path: Path) -> str | None:

    # Does path folder exist on the file system?
    if not path.exists():
        return f"Specified {{}} path not found. {path} is not a valid filesystem path."

    return validate_path_architecture(path)


def validate_target(path: Path) -> str | None:

    # Empty path should just be ignored
    if path.resolve() is None:
        return None

    # build a few of the files/folders we need for later
    namespace = path
    namespace_sounds = path / "sounds"
    minecraft = path.parent / "minecraft"
    sounds_json = minecraft / "sounds.json"

    # If path has an incomplete structure, create all necessary objects, if the user agrees
    if not namespace.exists() or \
       not namespace_sounds.exists() or \
       not minecraft.exists() or \
       not sounds_json.exists():

        response = input(f"\nPath {namespace} has an incomplete structure. Create folder structure? (y/N) ")
        if response.lower() != "y":
            return None

        # Create the proper folder structure in the target location
        namespace_sounds.mkdir(parents=True, exist_ok=True)
        minecraft.mkdir(parents=True, exist_ok=True)
        sounds_json.touch()

    # Validate existing structure
    return validate_path_architecture(path)


def validate_path_architecture(path: Path) -> str | None:

    # Folder in question must have only one child, and that child must be "sounds"
    path_check = [i for i in path.iterdir() if i.is_dir()]
    if len(path_check) != 1 and path_check[1] != "sounds":
        return f"The {{}} path {path} does not appear to be a namespace folder.  Should have a 'sounds' sub-folder."

    return None


def get_json_regex() -> str:
    volume: str = r'"volume":[0-1][.]\d|'
    pitch: str = r'"pitch":\d[.]\d|'
    weight: str = r'"weight":\d+|'
    stream: str = r'"stream":(?:true|false)|'
    dist: str = r'"attenuation_distance":\d+|'
    preload: str = r'"preload":(?:true|false)|'
    sound_type: str = r'"type":(?:"sound"|"event")'

    stage1 = r'(?:' + volume + pitch + weight + stream + dist + preload + sound_type + ')'
    stage2 = r'(?:,' + stage1 + ')*'

    result = r'^{' + stage1 + stage2 + '}$'

    return result


def include_patterns(*patterns):
    """ Function that can be used as shutil.copytree() ignore parameter that
    determines which files *not* to ignore, the inverse of "normal" usage.

    This is a factory function that creates a function which can be used as a
    callable for copytree()'s ignore argument, *not* ignoring files that match
    any of the glob-style patterns provided.

    ‛patterns’ are a sequence of pattern strings used to identify the files to
    include when copying the directory tree.

    Example usage:

        copytree(src_directory, dst_directory, ignore=include_patterns('*.ogg', '*.json'))

    Stolen from user martineau on Stack Overflow
    https://stackoverflow.com/questions/35155382/copying-specific-files-to-a-new-folder-while-maintaining-the-original-subdirect/35161407#35161407
    """
    def _ignore_patterns(path, all_names):

        # Set up files to keep based on incoming pattern(s)
        keep_files: set(str) = set()
        for p in patterns:
            g = (x.name for x in pathlib.Path(path).glob(p))
            keep_files.update(g)

        # Determine names which match one or more patterns (that shouldn't be ignored)
        keep = (name for pattern in patterns for name in keep_files)

        # Ignore file names which *didn't* match any of the patterns given that aren't directory names.
        dir_names = (name for name in all_names if (Path(path) / name).is_dir())

        return set(all_names) - set(keep) - set(dir_names)  # - set("generated-sounds.json")

    return _ignore_patterns


def get_event_dictionary(path: Path) -> dict[SoundEvent]:
    """Loads a json file from disk"""

    # If the file is empty, return an empty object
    if path.stat().st_size == 0:
        return {}

    with open(path, "r") as read_file:
        return dict(json.load(read_file))


def get_combined_json(source_events, target_path) -> dict[SoundEvent]:

    # If target is empty, just return source
    result = get_event_dictionary(target_path)
    if not result:
        return source_events

    # If target has something in it, loop through source
    for event_name, event_details in source_events.items():

        # if result doesn't contain that event yet, we just add all event details and move on
        if event_name not in result.keys():
            result[event_name] = event_details
            continue

        result[event_name]["replace"] = event_details["replace"]

        # Process sound files
        sounds: list = event_details["sounds"]
        test_list = [s for s in sounds if s not in result[event_name]["sounds"]]
        result[event_name]["sounds"].extend(test_list)

        result[event_name]["subtitle"] = event_details["subtitle"]

    # return empty structure, for now
    return result


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates a sounds.json file from a folder structure of .ogg files
    """

    args = handle_command_line()

    # Minecraft's regular expression for valid ogg file names/paths
    good_name = re.compile("^[a-z0-9/._-]+$")

    # Regular expression to validate sounds.json key-value pairs
    json_regex = re.compile(get_json_regex())

    warnings: list[str] = []

    source: Path = args.source
    namespace: str = args.source.name

    extensions: list[str] = [".ogg", ".subtitles"]
    sound_files: list[Path] = sorted([f for f in source.rglob('*') if f.suffix in extensions])
    # print(*sound_files, sep='\n')

    # Show me the maximum number of folders between "sounds" and the ogg file
    # This is an attempt to auto-detect the starting position of the sound event name
    max_list: tuple = max([x.parent.parts for x in sound_files], key=len)
    max_folders: int = len(max_list[max_list.index("sounds")+1:])

    # Build dictionary
    events: dict[str, SoundEvent] = {}
    known_events: list[str] = []
    for f in sound_files:

        # Only consider files under the "sounds" folder
        if "sounds" not in f.parts:
            warnings.append(f"{f}File is not under the 'sounds' folder")
            continue

        # Only consider files that match naming rules
        file_from_source: Path = f.relative_to(source.parent)
        if not good_name.match(str(file_from_source)):
            warnings.append(f"{file_from_source}\nPath does not match valid naming rules")
            continue

        # Strip off irrelevant bits from the path
        file: Path = f.relative_to(source / "sounds")

        # Build the event name
        typical_event_length = 3
        adj_index: int = max_folders - typical_event_length
        start_index: int = 0 if adj_index < 0 else adj_index
        event = ".".join(file.parent.parts[start_index:])

        # Initialize the event if we haven't seen it before
        if event not in known_events:

            # Build the event subtitle
            subtitle: str = f"subtitles.{file.stem[1:] if (file.suffix == '.subtitles') else event}"

            # Initialize the event
            known_events.append(event)
            events[event] = dict({"replace": True, "sounds": [], "subtitle": subtitle})
            # print(f"event: {event}")

        # build the sound dictionary, and add it to the sounds list
        if file.suffix == ".ogg":
            name: str = f"{namespace}:{file.parent}/{file.stem}"
            sound = OrderedDict({"name": name, "volume": 1.0})

            # Build the custom volume, pitch, weight or stream from sound file metadata
            album_title = TinyTag.get(f).album
            metadata = "" if not album_title else re.sub(r'\s+', '', album_title)

            # Only consider the metadata valid if it follows Minecraft's format
            if metadata and not json_regex.match(metadata):
                warnings.append(f"{f}\nFile metadata does not match Minecraft's format: {metadata}")
                continue

            # Only consider the metadata valid if it is valid JSON format
            try:
                tags: dict[Sound] = {} if not metadata else json.loads(metadata)
            except ValueError:
                warnings.append(f"{f}\nFile metadata is not valid JSON: ({metadata})")
                continue

            sound.update(tags)
            events[event]["sounds"].append(sound)
            # print(f"    {sound}")

    # Sort the dictionary by key?
    sorted_events = {key: val for key, val in sorted(events.items(), key=lambda ele: ele[0])}

    # If there are errors, display them and ask the user whether they'd like to proceed
    if len(warnings) > 0:
        print(f"\nThere were {len(warnings)} warnings during the process:")

        for w in warnings:
            print(f"\n{w}")

        response = input("\nWould you like to continue? (y/N) ")
        if response.lower() != "y":
            sys.exit()

    # Write the finished file to the source folder
    with open(source / "generated-sounds.json", "w") as fp:
        json.dump(sorted_events, fp, indent=4, cls=CompactJSONEncoder)

    # Show the user what was written to the source folder
    print(f"\nfile created in {source} with the following contents:\n")
    print(json.dumps(sorted_events, indent=4, cls=CompactJSONEncoder))

    # If the user hasn't specified a target folder, just get out
    if args.target.resolve() is None:
        sys.exit()

    # Ask the user whether we should copy files to the target folder
    print(f"\nTarget folder set to existing pack at:\n{args.target}")
    response = input("\nIncorporate these files into existing pack? (y/N) ")
    if response.lower() != "y":
        sys.exit()

    print("\n----------------------------------")
    print("Copying files to target location:")
    print("----------------------------------")

    # Copy OGG files to the target folder, creating folder structure if it doesn't exist
    shutil.copytree(args.source, args.target, ignore=include_patterns("*.ogg"), dirs_exist_ok=True)

    print("\nIncorporating JSON records into target sounds.json")

    target_json_file = args.target.parent / "minecraft" / "sounds.json"
    if target_json_file.resolve() is None:
        sys.exit("\nERROR: Target sounds.json file cannot be found.")

    # Combine JSON files
    # print("JSON combining code has yet to be written")
    combined_json = get_combined_json(sorted_events, target_json_file)

    # Write the finished file to the target folder
    with open(target_json_file, "w") as fp:
        json.dump(combined_json, fp, indent=4, cls=CompactJSONEncoder)

    # Show the user what was written to the target folder
    print(f"\nfile created in {target_json_file.parent} with the following contents:\n")
    print(json.dumps(sorted_events, indent=4, cls=CompactJSONEncoder, sort_keys=True))


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
