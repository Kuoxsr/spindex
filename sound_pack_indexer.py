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
into my config.fish:
export PYTHONPATH="$PYTHONPATH:{full path to tinytag sub-folder inside venv folder}"

Command-line arguments:

    --help      (-h)    Show usage
    --version   (-v)    Show version number
"""

__version__ = '0.41'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"


# Import modules
from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEvent, Sound

from enum import Enum
from json_encoder import CompactJSONEncoder
from pathlib import Path

import argparse
import json
import re
import shutil
import sys


class Color(str, Enum):

    green = "\033[32m"
    red = "\033[31m"
    cyan = "\033[36m"
    default = "\033[0m"


def handle_command_line(validate_source_function, validate_target_function):
    """
    Handle arguments supplied by the user
    """

    parser = argparse.ArgumentParser(
        prog="Sound Pack Indexer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Generates a json index from folders full of .ogg files. "
                    "\nOptionally allows automatic merging of this generated file with an existing pack.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __version__)

    parser.add_argument(
        "-i",
        "--index-only",
        action='store_true',
        help="Only produce the generated-sounds.json file and then exit.")

    parser.add_argument(
        "-q",
        "--quiet",
        action='store_true',
        help="Suppress printing of json file contents. Only show warnings.")

    parser.add_argument(
        "-a",
        "--abort-warnings",
        action='store_true',
        help="Treat all warnings as fatal errors, and exit as soon as they occur.")

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

    if src := validate_source_function(args.source):
        sys.exit(src.format("source"))

    if tgt := validate_target_function(args.target):
        sys.exit(tgt.format("target"))

    # resolve relative paths
    args.source = args.source.resolve()
    args.target = args.target.resolve()

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


def get_event_dictionary(path: Path) -> dict[str, SoundEvent]:
    """Loads a json file from disk"""

    # If the file is empty, return an empty object
    if path.stat().st_size == 0:
        return {}

    with open(path, "r") as read_file:
        return dict(json.load(read_file))


def process_ogg_files(files: list[Path]) -> tuple[list[Path], list[str]]:
    """
    Takes a list of ogg files and only keeps the ones that don't
    violate Minecraft's naming rules.  Generates warnings for any
    that do violate these rules.
    :param files: A list of files whose paths must start with the folder immediately under "sounds"
    :return: A tuple containing the list of valid files and a list of warnings
    """

    warnings: list[str] = []
    sound_paths: list[Path] = []

    # Minecraft's regular expression for valid ogg file names/paths
    mc_naming_rules = re.compile("^[a-z0-9/._-]+$")

    for file in files:

        # Only consider files that match naming rules
        if not mc_naming_rules.match(str(file)):
            warnings.append(f"{file} <- Path does not match valid naming rules, and will be ignored")
            continue

        sound_paths.append(file)

    return sound_paths, warnings


def get_combined_events(
        incoming_events: dict[str, SoundEvent],
        existing_events: dict[str, SoundEvent]) -> dict[str, SoundEvent]:

    result: dict[str, SoundEvent] = existing_events

    # Start by looping through the source dictionary
    for event_name, incoming_event_details in incoming_events.items():

        # if result doesn't contain that event yet, we just add all event details and move on
        if event_name not in result.keys():
            result[event_name] = incoming_event_details
            continue

        # Process sound files
        source_sounds: list = incoming_event_details["sounds"]
        new_sounds = [s for s in source_sounds if s not in result[event_name]["sounds"]]
        result[event_name]["sounds"].extend(new_sounds)

        # Sort the sounds by sound path name
        result[event_name]["sounds"] = sorted(result[event_name]["sounds"], key=lambda ele: ele["name"])

        # Only add a subtitle there is one, and if one doesn't already exist
        if "subtitle" in incoming_event_details and "subtitle" not in result[event_name]:
            result[event_name]["subtitle"] = incoming_event_details["subtitle"]

    # return empty structure, for now
    return dict(sorted(result.items()))


def get_generated_events(
        namespace: str,
        sound_files: list[Path],
        defaults: Defaults,
        sound_name_start_index: int) -> dict[str, SoundEvent]:
    """
    Takes a list of sound file paths and generates JSON records in the same format
     as a Minecraft sounds.json file

    :param namespace: The namespace to which all the ogg files belong
    :param sound_files: The list of .ogg file names in your folder structure
    :param defaults: A dictionary of default values for various parameters, built from a json file
    :param sound_name_start_index: Where the path should be trimmed to form the JSON that MC expects
    :return: A tuple containing the following items:
        A dictionary representing the json data to be written to sounds.json
        A list of warnings that occurred during the process
    """

    events: dict[str, SoundEvent] = {}
    known_events: list[str] = []

    # Build dictionary
    for file in sound_files:

        # Build the event name
        event_name = get_event_name(file)

        # Initialize the event if we haven't seen it before
        if event_name not in known_events:

            # Initialize the event
            known_events.append(event_name)
            events[event_name] = defaults.get_sound_event(event_name)

        # build the sound dictionary, and add it to the sounds list
        sound_name: str = f"{namespace}:{file.parent}/{file.stem}"

        sound = defaults.get_sound(event_name, sound_name)

        events[event_name]["sounds"].append(sound)

        # Sort the sounds by sound path name
        events[event_name]["sounds"] = sorted(events[event_name]["sounds"], key=lambda ele: ele["name"])

    # Sort the dictionary by key
    sorted_events: dict[str, SoundEvent] = {key: val for key, val in sorted(events.items(), key=lambda ele: ele[0])}
    return sorted_events


def get_event_name(ogg_file: Path) -> str:
    """
    Finds the event name from the file path, starting with
    an actual event starting segment.
    :param ogg_file: The file to use when building the event name
    :return: An event name formatted with dots (e.g.; entity.villager.ambient)
    """

    mc_event_start: list[str] = [
        "ambient",
        "block",
        "enchant",
        "entity",
        "event",
        "item",
        "music",
        "music_disc",
        "particle",
        "ui",
        "weather"
    ]

    event_parts: list[str] = []

    for part in ogg_file.parent.parts:

        if len(event_parts) > 0 or part in mc_event_start:

            # if we've already found the start, keep adding parts
            event_parts.append(part)

    # If there are less than two segments, it's probably not an event name
    if len(event_parts) < 2:
        return ""

    return ".".join(event_parts)


def check_for_overwritten_files(source_files: list[Path], target_files: list[Path]) -> list[str]:

    warnings: list[str] = list()

    # Loop through source list
    for file in source_files:

        # If the file will overwrite a file in the target, add its path to the warnings
        if file in target_files:
            warnings.append(f".../{file}")

    return warnings


def print_banner(title: str, info: str):

    bar = "-" * (len(title) + 1)
    print(f"{Color.green.value}\n{bar}\n{title}\n{bar}")
    print(f"{Color.cyan.value}{info}{Color.default.value}")


def print_warnings(warnings: list[str], header: str, action: str, abort_on_warnings: bool):

    # If there are no warnings, just get out
    if len(warnings) == 0:
        return

    print(f"\n{header}\n{Color.red.value}")

    for w in warnings:
        print(w)

    if abort_on_warnings:
        sys.exit(f"\n{Color.default.value}Script execution cannot continue.")

    response = input(f"{Color.default.value}\nWould you like to {action}? (y/N) ")
    if response.lower() != "y":
        print(Color.default.value)
        sys.exit()


def copy_sound_files(sound_files: list[Path], source_path: Path, target_path: Path):

    for file in sound_files:

        source = source_path / "sounds" / file
        target = target_path / "sounds" / file

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates a sounds.json file from a folder structure of .ogg files
    """

    args = handle_command_line(validate_source, validate_target)
    source_path: Path = args.source

    if not args.quiet:
        print_banner("Processing staging area ogg files:", f"Source folder: {source_path}")

    source_sound_path = source_path / "sounds"
    ogg_files: list[Path] = [f.relative_to(source_sound_path) for f in source_sound_path.rglob('*.ogg')]
    sound_files, warnings = process_ogg_files(ogg_files)
    print_warnings(
        warnings,
        f"There were {len(warnings)} warnings during the process:",
        "continue",
        args.abort_warnings)

    # Get the sound event defaults from the json file
    with open(source_path / 'defaults.json') as f:
        default_data = json.load(f)

    # Generate events from our .ogg files, and return any warnings that happened along the way
    generated_events = get_generated_events(
        source_path.name,
        sound_files,
        Defaults(default_data),
        1)

    # If nothing was generated, just get out
    if len(generated_events) == 0:
        if not args.quiet:
            print("\nNothing to process")
        sys.exit()

    # Write the finished file to the source folder
    with open(source_path / "generated-sounds.json", "w") as fp:
        json.dump(generated_events, fp, indent=4, cls=CompactJSONEncoder)

    # Show the user what was written to the source folder, unless in quiet mode
    if not args.quiet:
        print(f"\ngenerated-sounds.json contains the following contents:\n")
        print(json.dumps(generated_events, indent=4, cls=CompactJSONEncoder))

    # Just get out if index-only mode is set or if no target folder specified
    if args.index_only or args.target is None or args.target.resolve() is None:
        sys.exit()

    # Ask the user whether we should copy files to the target folder
    print(f"\nTarget folder set to existing pack at:\n{Color.cyan.value}{args.target}{Color.default.value}")
    response = input("\nIncorporate source files into existing pack? (y/N) ")
    if response.lower() != "y":
        sys.exit()

    if not args.quiet:
        print_banner("Copying files to target location:", f"Target folder: {args.target}")

    # pull lists of files from target
    target_sound_path = args.target / "sounds"
    target_files: list[Path] = list(f.relative_to(target_sound_path) for f in target_sound_path.rglob("*.ogg"))
    overwrite_warnings = check_for_overwritten_files(sound_files, target_files)
    print_warnings(
        overwrite_warnings,
        f"Files could be overwritten during this process.  {len(overwrite_warnings)} warning(s):",
        "overwrite these files",
        args.abort_warnings)

    # Copy OGG files to the target folder, creating folder structure if it doesn't exist
    copy_sound_files(sound_files, args.source, args.target)

    target_json_file = args.target.parent / "minecraft" / "sounds.json"

    if not args.quiet:
        print_banner(
            "Incorporating JSON records into target sounds.json:",
            f"Target file: {target_json_file}")

    if target_json_file.resolve() is None:
        sys.exit(f"{Color.red.value}\nERROR: Target sounds.json file cannot be found.{Color.default.value}")

    # Combine JSON files - If target is empty, just use source
    target_events = get_event_dictionary(target_json_file)
    combined_json = generated_events if not target_events else get_combined_events(generated_events, target_events)

    # Write the finished file to the target folder
    with open(target_json_file, "w") as fp:
        json.dump(combined_json, fp, indent=4, cls=CompactJSONEncoder)

    # Show the user what was written to the target folder, unless in quiet mode
    if not args.quiet:
        print(f"\nCombined file has the following contents:\n")
        print(json.dumps(combined_json, indent=4, cls=CompactJSONEncoder, sort_keys=True))


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
