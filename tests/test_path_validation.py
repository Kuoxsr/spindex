from pathlib import Path

import pytest

from spindex import IncorrectDirStructureError
from spindex import validate_target_path
from spindex import validate_source_path


def test_validate_source_path_should_raise_error_when_path_does_not_exist():

    path: Path = Path("/test/folder/namespace")

    with pytest.raises(FileNotFoundError) as error:
        validate_source_path(path)

    result: str = str(error.value)
    assert (result == "Specified source path not found. "
                      "/test/folder/namespace is not a valid filesystem path.")


def test_validate_source_path_should_raise_error_when_no_sounds_folder_exists(fs):

    fs.create_dir("/test/folder/namespace/not-sounds")

    path: Path = Path("/test/folder/namespace")

    with pytest.raises(IncorrectDirStructureError) as error:
        validate_source_path(path)

    result: str = str(error.value)
    assert result == ("/test/folder/namespace "
                      "does not appear to be a namespace folder. "
                      "Should have a 'sounds' sub-folder.")


def test_validate_source_path_should_raise_error_when_sounds_folder_not_alone(fs):

    fs.create_dir("/test/folder/namespace/sounds")
    fs.create_dir("/test/folder/namespace/other-folder")

    path: Path = Path("/test/folder/namespace")

    with pytest.raises(IncorrectDirStructureError) as error:
        validate_source_path(path)

    result: str = str(error.value)
    assert result == ("/test/folder/namespace "
                      "does not appear to be a namespace folder. "
                      "Should only have one sub-folder.")


def test_validate_source_path_should_not_raise_error_when_proper_structure(fs):

    fs.create_dir("/test/folder/namespace/sounds")

    path: Path = Path("/test/folder/namespace")

    try:
        validate_source_path(path)
    except Exception as exc:
        assert False, f"Unexpected exception: {exc}"

# ------------------------------------------------------------------------


def test_validate_target_path_should_raise_system_exit_when_user_aborts(fs, monkeypatch):

    fs.create_dir("/test/folder")
    monkeypatch.setattr(target="builtins.input", name=lambda prompt: "n")

    path: Path = Path("/test/folder")

    with pytest.raises(SystemExit) as error:
        validate_target_path(path)

    result = str(error.value)
    assert result == "Aborted by user."


def test_validate_target_path_should_create_dir_structure_when_user_confirms(fs, monkeypatch):

    fs.create_dir("/test/folder")
    monkeypatch.setattr(target="builtins.input", name=lambda prompt: "y")

    path: Path = Path("/test/folder")

    try:
        validate_target_path(path)
    except Exception as exc:
        assert False, f"Unexpected exception: {exc}"

    namespace = path
    namespace_sounds = path / "sounds"
    minecraft = path.parent / "minecraft"
    sounds_json = minecraft / "sounds.json"

    if any([not namespace.exists(),
            not namespace_sounds.exists(),
            not minecraft.exists(),
            not sounds_json.exists()]):

        assert False, "Structure not created successfully"

# ------------------------------------------------------------------------
