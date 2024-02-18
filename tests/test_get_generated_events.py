from pathlib import Path

from objects.defaults import Defaults
from objects.sound_event_catalog import SoundEventCatalog
from objects.typed_dictionaries import SoundEventDefaults, Sound
from sound_pack_indexer import get_generated_events


def test_get_generated_events_should_build_event_name_correctly():

    namespace = "test-namespace"

    file1 = Path("entity/villager/ambient/test-ogg-file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 1
    assert len(warnings) == 0
    assert "entity.villager.ambient" in result


def test_get_generated_events_should_build_sound_name_correctly():

    namespace = "test-namespace"

    file1 = Path("entity/witch/celebrate/test-ogg-file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    expected_sound = [Sound(name=f"{namespace}:{file1}")]

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert result["entity.witch.celebrate"]["sounds"] == expected_sound


def test_get_generated_events_should_separate_paths_into_different_events():

    namespace = "test-namespace"

    file1 = Path("entity/villager/celebrate/test-ogg-file")
    file2 = Path("entity/witch/death/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 2
    assert len(warnings) == 0
    assert "entity.villager.celebrate" in result
    assert "entity.witch.death" in result


def test_get_generated_events_should_place_sounds_in_the_same_path_into_the_same_event():

    namespace = "test-namespace"

    file1 = Path("entity/villager/death/test-ogg-file")
    file2 = Path("entity/villager/death/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result["entity.villager.death"]["sounds"]) == 2


def test_get_generated_events_should_sort_sound_names_alphabetically():

    namespace = "test-namespace"

    file1 = Path("entity/villager/trade/test-ogg-file")
    file2 = Path("entity/villager/trade/ogg_file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    expected_sound1 = Sound(name=f"{namespace}:{file2}")
    expected_sound2 = Sound(name=f"{namespace}:{file1}")

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert result["entity.villager.trade"]["sounds"][0] == expected_sound1
    assert result["entity.villager.trade"]["sounds"][1] == expected_sound2


def test_get_generated_events_should_sort_event_names_alphabetically():

    namespace = "test-namespace"

    file1 = Path("entity/witch/hurt/ogg_file")
    file2 = Path("entity/villager/no/test_ogg-file")
    sound_files: list[Path] = [file1, file2]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 2
    assert len(warnings) == 0
    assert list(result) == ["entity.villager.no", "entity.witch.hurt"]


def test_get_generated_events_should_return_warning_when_path_is_only_partially_correct():

    namespace = "test-namespace"

    file1 = Path("entity/not/so/much/ogg_file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 0
    assert len(warnings) == 1
    assert warnings[0] == "The constructed event name (entity.not.so.much) was not found in catalog"


def test_get_generated_events_should_return_warning_when_path_is_completely_incorrect():

    namespace = "test-namespace"

    file1 = Path("not/so/much/ogg_file")
    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 0
    assert len(warnings) == 1
    assert warnings[0] == f"Could not build a sound event from this path: {file1}"


def test_get_generated_events_should_return_partial_results_when_mixed_warnings_and_successes():

    namespace = "test-namespace"

    file1 = Path("entity/partially/bad/path/ogg_file1")
    file2 = Path("entity/villager/celebrate/ogg_file2")
    file3 = Path("totally/bad/file/path/ogg_file3")
    sound_files: list[Path] = [file1, file2, file3]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    result, warnings = get_generated_events(namespace, sound_files, defaults, SoundEventCatalog())
    assert len(result) == 1
    assert list(result) == ["entity.villager.celebrate"]
    assert len(warnings) == 2
    assert warnings[0] == "The constructed event name (entity.partially.bad.path) was not found in catalog"
    assert warnings[1] == f"Could not build a sound event from this path: {file3}"


