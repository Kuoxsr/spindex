#!/usr/bin/env python3

# noinspection GrazieInspection
"""
Problem: Automatically generate a Minecraft sounds.json file from a folder structure
Target Users: Me
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Take a series of .ogg files and create the JSON to describe it
Notes:

Command-line arguments:

    --help      (-h)    Show usage
    --version   (-v)    Show version number
"""

__version__ = '0.5'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
from json_encoder import CompactJSONEncoder
from pathlib import Path
import argparse
import json


def handle_command_line():
    """
    Handle arguments supplied by the user
    """

    parser = argparse.ArgumentParser(
        prog="Sound Pack Checker",
        description="generates lists of invalid connections between json and sound files.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __version__)

    parser.add_argument(
        "path",
        action="store",
        nargs=argparse.REMAINDER,
        help="Path to the sounds.json file you want to check.  The file name itself is not required.")

    args = parser.parse_args()

    # path is a LIST at this point, and we want just a string
    if len(args.path) > 0:
        args.path = args.path[0]
    else:
        args.path = ""

    # If the user doesn't specify a path, use current working directory
    if not args.path:
        args.path = Path.cwd()

    # If the user specifies a string, make sure it's a path object
    path = Path(args.path)

    # Does path folder exist on the file system?
    if not path.exists():
        print(f"Specified path not found. {path} is not a valid filesystem path.")
        exit()

    # Finally, make the argument a Path  (does this work?)
    args.path = Path(args.path).resolve()

#    print("args:",args); exit()
    return args


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates a sounds.json file from a folder structure of .ogg files
    """

    args = handle_command_line()

    target: Path = args.path
    namespace: str = args.path.name

    extensions: list[str] = [".ogg", ".subtitles"]
    sound_files: list[Path] = sorted([f for f in target.rglob('*') if f.suffix in extensions])
    # print(*sound_files, sep='\n')

    # Show me the maximum number of folders between "sounds" and the ogg file
    # This is an attempt to auto-detect the starting position of the sound event name
    max_folders: int = 0
    for x in sound_files:
        test = x.relative_to(target).parent.parts
        if len(test) > max_folders:
            max_folders = len(test)

    # Build dictionary
    events: dict[str, dict[str, bool | list[dict[str, str | float]]], str] = {}
    known_events: list[str] = []
    for file in sound_files:

        # Only consider files under the "sounds" folder
        if "sounds" not in file.parts:
            continue

        # Build the event name
        start_index: int = (max_folders >= 5) + 1
        parts = file.relative_to(target).parent.parts[start_index:]
        event = ".".join(parts)

        # Initialize the event if we haven't seen it before
        if event not in known_events:

            # Build the event subtitle
            subtitle: str = "subtitles."
            if file.suffix == ".subtitles":
                subtitle += file.stem[1:]
            else:
                subtitle += event

            # Initialize the event
            known_events.append(event)
            events[event] = dict({"replace": True, "sounds": [], "subtitle": subtitle})
            # print(f"event: {event}")

        # build the sound dictionary, and add it to the sounds list
        if file.suffix == ".ogg":
            name: str = f"{namespace}:{'/'.join(file.relative_to(target).parts[1:-1])}/{file.stem}"
            sound: dict[str, str | float] = dict({"name": name, "volume": 0.5})
            events[event]["sounds"].append(sound)
            # print(f"    {sound}")

    # Sort the dictionary by key?
    sorted_events = {key: val for key, val in sorted(events.items(), key=lambda ele: ele[0])}

    with open("generated-sounds.json", "w") as fp:
        json.dump(sorted_events, fp, indent=4, cls=CompactJSONEncoder)

    print(f"\nfile created in {target} with the following contents:\n")
    print(json.dumps(sorted_events, indent=4, cls=CompactJSONEncoder))


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
