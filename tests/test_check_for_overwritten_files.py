from pathlib import Path

from sound_pack_indexer import check_for_overwritten_files


def test_check_for_overwritten_files_should_not_warn_when_no_files_in_target():

    # Arrange
    source_files: list[Path] = [Path("entity/villager/ambient/file01.ogg")]
    target_files: list[Path] = []

    # Act
    warnings = check_for_overwritten_files(source_files, target_files)

    # Assert
    assert len(warnings) == 0


def test_check_for_overwritten_files_should_not_warn_when_path_is_different():

    # Arrange
    source_files: list[Path] = [Path("entity/villager/ambient/file01.ogg")]
    target_files: list[Path] = [Path("entity/villager/hurt/file01.ogg")]

    # Act
    warnings = check_for_overwritten_files(source_files, target_files)

    # Assert
    assert len(warnings) == 0


def test_check_for_overwritten_files_should_not_warn_when_file_name_is_different():

    # Arrange
    source_files: list[Path] = [Path("entity/villager/ambient/file01.ogg")]
    target_files: list[Path] = [Path("entity/villager/ambient/file02.ogg")]

    # Act
    warnings = check_for_overwritten_files(source_files, target_files)

    # Assert
    assert len(warnings) == 0


def test_check_for_overwritten_files_should_warn_when_file_name_is_identical():

    # Arrange
    source_files: list[Path] = [Path("entity/villager/ambient/file01.ogg")]
    target_files: list[Path] = [Path("entity/villager/ambient/file01.ogg")]

    # Act
    warnings = check_for_overwritten_files(source_files, target_files)

    # Assert
    assert len(warnings) == 1
    assert warnings[0] == f".../{source_files[0]}"


def test_check_for_overwritten_files_should_warn_for_multiple_collisions():

    # Arrange
    source_files: list[Path] = [
        Path("entity/villager/ambient/file02.ogg"),
        Path("entity/villager/ambient/file03.ogg"),
        Path("entity/villager/ambient/file04.ogg")
    ]

    target_files: list[Path] = [
        Path("entity/villager/ambient/file01.ogg"),
        Path("entity/villager/ambient/file02.ogg"),
        Path("entity/villager/ambient/file04.ogg")
    ]

    # Act
    warnings = check_for_overwritten_files(source_files, target_files)

    # Assert
    assert len(warnings) == 2
    assert warnings[0] == f".../{source_files[0]}"
    assert warnings[1] == f".../{source_files[2]}"
