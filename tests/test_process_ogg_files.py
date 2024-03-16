
from pathlib import Path
from spindex import process_ogg_files


def test_process_ogg_files_should_generate_warning_for_a_bad_file_name():

    # Arrange file paths that involve all characters that Minecraft supports
    good_file_name = Path("entity/villager/ambient/abc012._-zyx.ogg")
    bad_file_name = Path("entity/villager/ambient/Xyz-_.210bca.ogg")

    files: list[Path] = [good_file_name, bad_file_name]

    result, warnings = process_ogg_files(files)
    assert len(result) == 1
    assert result[0] == Path("entity/villager/ambient/abc012._-zyx.ogg")
    assert len(warnings) == 1
    assert warnings[0] == f"{bad_file_name} <- Path does not match valid naming rules, and will be ignored"
