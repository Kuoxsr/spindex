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

__version__ = '0.35'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEvent, Sound

from json_encoder import CompactJSONEncoder
from pathlib import Path

import argparse
import json
import re
import shutil
import sys


def handle_command_line():
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

    if src := validate_source(args.source):
        sys.exit(src.format("source"))

    if tgt := validate_target(args.target):
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


def everything_but_ogg_files():
    """ Function that can be used as a shutil.copytree() ignore parameter that
    determines which files *not* to ignore, the inverse of "normal" usage.

    This is a factory function that creates a function which can be used as a
    callable for copytree()'s ignore argument, *not* ignoring files that match
    any of the glob-style patterns provided.

    Stolen from user martineau on Stack Overflow, and heavily modified for my own use-case
    https://stackoverflow.com/a/35161407
    """
    def _ignore_patterns(path, all_names):

        files_to_ignore: set[str] = set()
        for name in all_names:

            name_to_check = (Path(path) / name)

            # Handle differently if name is a directory
            if name_to_check.is_dir():

                # If there are no .ogg files in any of the directory's subdirectories
                if len([x for x in name_to_check.rglob('*.ogg')]) == 0:
                    files_to_ignore.add(name)

                continue

            # Ignore files that are not .ogg
            if name_to_check.suffix != '.ogg':
                files_to_ignore.add(name)

        return set(files_to_ignore)

    return _ignore_patterns


def get_event_dictionary(path: Path) -> dict[str, SoundEvent]:
    """Loads a json file from disk"""

    # If the file is empty, return an empty object
    if path.stat().st_size == 0:
        return {}

    with open(path, "r") as read_file:
        return dict(json.load(read_file))


def process_ogg_files(files: list[Path]) -> tuple[list[Path], list[str]]:

    warnings: list[str] = []
    sound_paths: list[Path] = []

    # Minecraft's regular expression for valid ogg file names/paths
    mc_naming_rules = re.compile("^[a-z0-9/._-]+$")

    for file in files:

        # Only consider files that match naming rules
        if not mc_naming_rules.match(str(file)):
            warnings.append(f"{file}\nPath does not match valid naming rules")
            continue

        # Only consider files that are beneath the "sounds" folder
        if "sounds" not in file.parts:
            warnings.append(f'{file}\nFile is not beneath the "sounds" folder')
            continue

        # Strip off irrelevant bits from the path
        sound_path: Path = file.relative_to("/".join(file.parts[0:2]))
        sound_paths.append(sound_path)

    return sound_paths, warnings


def get_sound_name_start_index(sound_files: list[Path]) -> int:

    # Show me the maximum number of folders between "sounds" and the ogg file
    # This is an attempt to auto-detect the starting position of the sound event name
    max_list: tuple = max([x.parent.parts for x in sound_files], key=len)
    max_folders: int = len(max_list[max_list.index("sounds")+1:])

    # Calculate the starting index of the file path that belongs in the json data
    typical_event_length = 3
    adj_index: int = max_folders - typical_event_length
    return 0 if adj_index < 0 else adj_index


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
        event_name = ".".join(file.parent.parts[sound_name_start_index:])

        # Initialize the event if we haven't seen it before
        if event_name not in known_events:

            # Initialize the event
            known_events.append(event_name)
            events[event_name] = defaults.get_sound_event(event_name)

        # build the sound dictionary, and add it to the sounds list
        sound_name: str = f"{namespace}:{file.parent}/{file.stem}"

        sound = defaults.get_sound(event_name, sound_name)

        events[event_name]["sounds"].append(sound)

    # Sort the dictionary by key
    sorted_events: dict[str, SoundEvent] = {key: val for key, val in sorted(events.items(), key=lambda ele: ele[0])}
    return sorted_events


def get_string_path_relative_to_sounds_folder(path: Path) -> str:

    # Find index of "sounds" folder
    sounds_index: int = path.parts.index("sounds")

    # build string based on the parts that are relative to the index
    return "/".join(path.parts[sounds_index:])


def check_for_overwritten_files(source_path, target_path) -> list[str]:

    warnings: list[str] = list()

    # pull lists of files from both source and target
    source_files: list[str] = list(get_string_path_relative_to_sounds_folder(f) for f in source_path.rglob("*.ogg"))
    target_files: list[str] = list(get_string_path_relative_to_sounds_folder(f) for f in target_path.rglob("*.ogg"))

    # Loop through source list
    for file in source_files:

        # If the file will overwrite a file in the target, add its path to the warnings
        if file in target_files:
            warnings.append(f".../{file}")

    return warnings


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates a sounds.json file from a folder structure of .ogg files
    """

    green = "\033[32m"
    red = "\033[31m"
    cyan = "\033[36m"
    default = "\033[0m"

    args = handle_command_line()
    source_path: Path = args.source

    if not args.quiet:
        print(f"{green}\n-----------------------------------")
        print("Processing staging area ogg files:")
        print(f"-----------------------------------{default}")
        print(f"{cyan}Source folder: {source_path}{default}")

    ogg_files: list[Path] = [f.relative_to(source_path.parent) for f in source_path.rglob('*.ogg')]
    sound_files, warnings = process_ogg_files(ogg_files)

    # If there are errors, display them and ask the user whether they'd like to proceed
    if len(warnings) > 0:
        print(f"\nThere were {len(warnings)} warnings during the process:{red}")

        for w in warnings:
            print(w)

        if args.abort_warnings:
            sys.exit(f"\n{default}Script execution cannot continue.")

        response = input(f"{default}\nWould you like to continue? (y/N) ")
        if response.lower() != "y":
            print(default)
            sys.exit()

    # Get the sound event defaults from the json file
    with open(source_path / 'defaults.json') as f:
        default_data = json.load(f)

    # Generate events from our .ogg files, and return any warnings that happened along the way
    generated_events, warnings = get_generated_events(
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
    print(f"\nTarget folder set to existing pack at:\n{cyan}{args.target}{default}")
    response = input("\nIncorporate source files into existing pack? (y/N) ")
    if response.lower() != "y":
        sys.exit()

    if not args.quiet:
        print(f"{green}\n\n----------------------------------")
        print("Copying files to target location:")
        print(f"----------------------------------{default}")
        print(f"{cyan}Target folder: {args.target}{default}")

    overwrite_warnings = check_for_overwritten_files(args.source, args.target)
    if len(overwrite_warnings) > 0:
        print(f"\nFiles could be overwritten during this process.  {len(overwrite_warnings)} warning(s):\n{red}")

        for w in overwrite_warnings:
            print(w)

        if args.abort_warnings:
            sys.exit(f"\n{default}Script execution cannot continue.")

        response = input(f"{default}\nWould you like to overwrite these files? (y/N) ")
        if response.lower() != "y":
            print(default)
            sys.exit()

    # Copy OGG files to the target folder, creating folder structure if it doesn't exist
    shutil.copytree(args.source, args.target, ignore=everything_but_ogg_files(), dirs_exist_ok=True)

    target_json_file = args.target.parent / "minecraft" / "sounds.json"

    if not args.quiet:
        print(f"{green}\n\n----------------------------------------------------")
        print("Incorporating JSON records into target sounds.json:")
        print(f"----------------------------------------------------{default}")
        print(f"{cyan}Target file: {target_json_file}{default}")

    if target_json_file.resolve() is None:
        sys.exit(f"{red}\nERROR: Target sounds.json file cannot be found.{default}")

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
