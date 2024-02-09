from pathlib import Path

from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEventDefaults, SoundEvent, Sound
from sound_pack_indexer import get_generated_events


def test_get_generated_events_should_build_event_name_correctly():

    namespace = "test-namespace"

    file1 = Path("one/two/three/test-ogg-file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert len(result) == 1
    assert "one.two.three" in result


def test_get_generated_events_should_build_sound_name_correctly():

    namespace = "test-namespace"

    file1 = Path("one/two/three/test-ogg-file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    expected_sound = [Sound(name=f"{namespace}:one/two/three/test-ogg-file")]

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert result["one.two.three"]["sounds"] == expected_sound


def test_get_generated_events_should_separate_paths_into_different_events():

    namespace = "test-namespace"

    file1 = Path("one/two/three/test-ogg-file")
    file2 = Path("three/two/one/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert len(result) == 2
    assert "one.two.three" in result
    assert "three.two.one" in result


def test_get_generated_events_should_place_sounds_in_the_same_path_into_the_same_event():

    namespace = "test-namespace"

    file1 = Path("one/two/three/test-ogg-file")
    file2 = Path("one/two/three/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert len(result["one.two.three"]["sounds"]) == 2


def test_get_generated_events_should_sort_sound_names_alphabetically():

    namespace = "test-namespace"

    file1 = Path("one/two/three/test-ogg-file")
    file2 = Path("one/two/three/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    expected_sound1 = Sound(name=f"{namespace}:one/two/three/ogg_file")
    expected_sound2 = Sound(name=f"{namespace}:one/two/three/test-ogg-file")

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert result["one.two.three"]["sounds"][0] == expected_sound1
    assert result["one.two.three"]["sounds"][1] == expected_sound2


def test_get_generated_events_should_sort_event_names_alphabetically():

    namespace = "test-namespace"

    file1 = Path("three/two/one/test_ogg_file")
    file2 = Path("one/two/three/ogg-file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert len(result) == 2
    assert list(result) == ["one.two.three", "three.two.one"]


