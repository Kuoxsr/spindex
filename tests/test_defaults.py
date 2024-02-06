
from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEventDefaults, Sound, SoundEvent
import pytest


def test_get_sound_event_should_use_event_replace():

    event_defaults = SoundEventDefaults(replace=False)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound_event("test.event")
    assert result["replace"] is False


def test_get_sound_event_should_use_event_replace_instead_of_all():

    all_defaults = SoundEventDefaults(replace=True)
    event_defaults = SoundEventDefaults(replace=False)
    defaults = Defaults({"all": all_defaults, "test.event": event_defaults})

    result = defaults.get_sound_event("test.event")
    assert result["replace"] is False


def test_get_sound_event_should_use_all_when_no_event_replace_exists():

    all_defaults = SoundEventDefaults(replace=True)
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound_event("test.event")
    assert result["replace"] is True


def test_get_sound_event_should_return_empty_list_for_sounds():

    defaults = Defaults({"test.event": SoundEventDefaults()})

    result = defaults.get_sound_event("test.event")
    assert result["sounds"] == []


def test_get_sound_event_should_use_event_subtitle():

    event_defaults = SoundEventDefaults(subtitle="test.subtitle")
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound_event("test.event")
    assert result["subtitle"] == "subtitles.test.subtitle"


def test_get_sound_event_should_use_event_name_for_subtitle_when_no_event_subtitle_exists():

    defaults = Defaults({"test.event": SoundEventDefaults()})

    result = defaults.get_sound_event("test.event")
    assert result["subtitle"] == "subtitles.test.event"


def test_get_sound_event_should_not_honor_subtitle_defaulted_under_all():

    event_defaults = SoundEventDefaults(subtitle="test.subtitle")
    defaults = Defaults({"all": event_defaults})

    result = defaults.get_sound_event("test.event")
    assert result["subtitle"] == "subtitles.test.event"


def test_get_sound():
    assert True
