from pathlib import Path

from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEventDefaults, SoundEvent, Sound
from sound_pack_indexer import get_generated_events


def test_get_generated_events_should_built_event_name_correctly():

    namespace = "test-namespace"

    # Arrange file paths that involve all characters that Minecraft supports
    file1 = Path("one/two/three/test-ogg-file")

    sound_files: list[Path] = [file1]

    # Dummy defaults object with neither the event we're testing nor "all"
    defaults = Defaults({"test": SoundEventDefaults()})

    sound_name_start_index = 0

    expected_sound = [Sound(name=f"{namespace}:one/two/three/test-ogg-file")]
    expected = SoundEvent(sounds=expected_sound, subtitle="subtitles.one.two.three")

    result = get_generated_events(namespace, sound_files, defaults, sound_name_start_index)
    assert result["one.two.three"] == expected


