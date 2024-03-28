import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from spindex import handle_command_line


def test_handle_command_line_should_parse_correct_arguments_correctly():

    test_arguments = [
        "sound_pack_indexer",
        "-i",
        "-q",
        "-a",
        "-s",
        "/path/to/source/files/",
        "-t",
        "/path/to/target/"
    ]

    with patch.object(sys, 'argv', test_arguments):
        args = handle_command_line()

        assert args.index_only is True
        assert args.quiet is True
        assert args.abort_warnings is True
        assert args.source == Path("/path/to/source/files/")
        assert args.target == Path("/path/to/target")


def test_handle_command_line_should_parse_long_arguments_correctly():

    test_arguments = [
        "sound_pack_indexer",
        "--index-only",
        "--quiet",
        "--abort-warnings",
        "--source",
        "/path/to/source/files/",
        "--target",
        "/path/to/target/"
    ]

    with patch.object(sys, 'argv', test_arguments):
        args = handle_command_line()

        assert args.index_only is True
        assert args.quiet is True
        assert args.abort_warnings is True
        assert args.source == Path("/path/to/source/files/")
        assert args.target == Path("/path/to/target")


def test_handle_command_line_should_report_unknown_switches(capsys):

    test_arguments = ["sound_pack_indexer", "-y"]

    with (patch.object(sys, 'argv', test_arguments)):

        with pytest.raises(SystemExit) as excinfo:
            args = handle_command_line()

        assert excinfo.value.code == 2

        captured = capsys.readouterr()
        assert captured.err == (
            "usage: Sound Pack Indexer [-h] [-v] [-i] [-q] [-a] [-s SOURCE] [-t TARGET]\n"
            "Sound Pack Indexer: error: unrecognized arguments: -y\n"
        )

