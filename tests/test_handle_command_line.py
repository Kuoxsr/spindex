import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from sound_pack_indexer import handle_command_line


@pytest.fixture
def validate_source_success():
    def validate_source_function(*args):
        return None

    return validate_source_function


@pytest.fixture
def validate_target_success():
    def validate_target_function(*args):
        return None

    return validate_target_function


@pytest.fixture
def validate_source_failure():
    def validate_source_function(*args):
        return "source failed"

    return validate_source_function


@pytest.fixture
def validate_target_failure():
    def validate_target_function(*args):
        return "target failed"

    return validate_target_function


def test_handle_command_line_should_parse_correct_arguments_correctly(validate_source_success, validate_target_success):

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
        args = handle_command_line(validate_source_success, validate_target_success)

        assert args.index_only is True
        assert args.quiet is True
        assert args.abort_warnings is True
        assert args.source == Path("/path/to/source/files/")
        assert args.target == Path("/path/to/target")


def test_handle_command_line_should_parse_long_arguments_correctly(validate_source_success, validate_target_success):

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
        args = handle_command_line(validate_source_success, validate_target_success)

        assert args.index_only is True
        assert args.quiet is True
        assert args.abort_warnings is True
        assert args.source == Path("/path/to/source/files/")
        assert args.target == Path("/path/to/target")


def test_handle_command_line_should_report_unknown_switches(capsys, validate_source_success, validate_target_success):

    test_arguments = ["sound_pack_indexer", "-y"]

    with (patch.object(sys, 'argv', test_arguments)):

        with pytest.raises(SystemExit) as excinfo:
            args = handle_command_line(validate_source_success, validate_target_success)

        assert excinfo.value.code == 2

        captured = capsys.readouterr()
        assert captured.err == (
            "usage: Sound Pack Indexer [-h] [-v] [-i] [-q] [-a] [-s SOURCE] [-t TARGET]\n"
            "Sound Pack Indexer: error: unrecognized arguments: -y\n"
        )


def test_handle_command_line_should_abort_on_source_path_error(capsys, validate_source_failure, validate_target_success):

    test_arguments = ["sound_pack_indexer", "-s", "/this/is/a/source/path/"]

    with (patch.object(sys, 'argv', test_arguments)):

        with pytest.raises(SystemExit) as excinfo:
            args = handle_command_line(validate_source_failure, validate_target_success)

        assert excinfo.value.code == "source failed"


def test_handle_command_line_should_abort_on_target_path_error(capsys, validate_source_success, validate_target_failure):

    test_arguments = ["sound_pack_indexer", "-s", "/this/is/a/source/path/", "-t", "/this/is/the/target/"]

    with (patch.object(sys, 'argv', test_arguments)):

        with pytest.raises(SystemExit) as excinfo:
            args = handle_command_line(validate_source_success, validate_target_failure)

        assert excinfo.value.code == "target failed"

