from pathlib import Path
from objects.sound_event_catalog import SoundEventCatalog, SoundEventValueError

import pytest


def test_sound_event_catalog_get_sound_event_name_should_return_correct_name():

    path: Path = Path("/good/path/weird/entity/villager/ambient/ogg_file_name")

    catalog = SoundEventCatalog()
    result = catalog.get_sound_event_name(path)

    assert result == "entity.villager.ambient"


def test_sound_event_catalog_get_sound_event_name_should_raise_error_when_constructed_path_incorrect():

    path: Path = Path("/path/weird/entity/villager/whatever/ogg_file_name")

    catalog = SoundEventCatalog()

    with pytest.raises(SoundEventValueError) as result:
        catalog.get_sound_event_name(path)

    assert str(result.value) == "The constructed event name (entity.villager.whatever) was not found in catalog"


def test_sound_event_catalog_get_sound_event_name_should_raise_error_when_event_name_cannot_be_constructed():

    path: Path = Path("/not/really/a/sound/event_name/ogg_file_name")

    catalog = SoundEventCatalog()

    with pytest.raises(SoundEventValueError) as result:
        catalog.get_sound_event_name(path)

    assert str(result.value) == f"Could not build a sound event from this path: {path}"
