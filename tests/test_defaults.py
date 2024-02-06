
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

# ------------------------------------------------------------------------


def test_get_sound_event_should_return_empty_list_for_sounds():

    defaults = Defaults({"test.event": SoundEventDefaults()})

    result = defaults.get_sound_event("test.event")
    assert result["sounds"] == []

# ------------------------------------------------------------------------


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

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_volume():

    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["volume"] == 0.1


def test_get_sound_should_use_event_volume_instead_of_all():

    all_defaults = SoundEventDefaults(volume=0.9)
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_defaults, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["volume"] == 0.1


def test_get_sound_should_use_all_when_no_event_volume_exists():

    all_defaults = SoundEventDefaults(volume=0.9)
    event_defaults = SoundEventDefaults(weight=8)
    defaults = Defaults({"all": all_defaults, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["volume"] == 0.9


def test_get_sound_should_not_include_volume_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "volume" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_weight():

    event_defaults = SoundEventDefaults(weight=8)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["weight"] == 8


def test_get_sound_should_use_event_weight_instead_of_all():

    all_details = SoundEventDefaults(weight=1)
    event_defaults = SoundEventDefaults(weight=8)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["weight"] == 8


def test_get_sound_should_use_all_when_no_event_weight_exists():

    all_details = SoundEventDefaults(weight=1)
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["weight"] == 1


def test_get_sound_should_not_include_weight_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "weight" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_pitch():

    event_defaults = SoundEventDefaults(pitch=1.3)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["pitch"] == 1.3


def test_get_sound_should_use_event_pitch_instead_of_all():

    all_details = SoundEventDefaults(pitch=5.4)
    event_defaults = SoundEventDefaults(pitch=1.3)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["pitch"] == 1.3


def test_get_sound_should_use_all_when_no_event_pitch_exists():

    all_details = SoundEventDefaults(pitch=5.4)
    event_defaults = SoundEventDefaults(volume=1.3)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["pitch"] == 5.4


def test_get_sound_should_not_include_pitch_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "pitch" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_stream():

    event_defaults = SoundEventDefaults(stream=True)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["stream"] is True


def test_get_sound_should_use_event_stream_instead_of_all():

    all_details = SoundEventDefaults(stream=False)
    event_defaults = SoundEventDefaults(stream=True)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["stream"] is True


def test_get_sound_should_use_all_when_no_event_stream_exists():

    all_details = SoundEventDefaults(stream=False)
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["stream"] is False


def test_get_sound_should_not_include_stream_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "stream" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_attenuation():

    event_defaults = SoundEventDefaults(attenuation_distance=3)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["attenuation_distance"] == 3


def test_get_sound_should_use_event_attenuation_instead_of_all():

    all_details = SoundEventDefaults(attenuation_distance=42)
    event_defaults = SoundEventDefaults(attenuation_distance=3)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["attenuation_distance"] == 3


def test_get_sound_should_use_all_when_no_event_attenuation_exists():

    all_details = SoundEventDefaults(attenuation_distance=42)
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["attenuation_distance"] == 42


def test_get_sound_should_not_include_attenuation_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "attenuation_distance" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_preload():

    event_defaults = SoundEventDefaults(preload=True)
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["preload"] is True


def test_get_sound_should_use_event_preload_instead_of_all():

    all_details = SoundEventDefaults(preload=False)
    event_defaults = SoundEventDefaults(preload=True)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["preload"] is True


def test_get_sound_should_use_all_when_no_event_preload_exists():

    all_details = SoundEventDefaults(preload=False)
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["preload"] is False


def test_get_sound_should_not_include_preload_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "preload" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_use_event_type():

    event_defaults = SoundEventDefaults(type="event type")
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "event type"


def test_get_sound_should_use_event_type_instead_of_all():

    all_details = SoundEventDefaults(type="all type")
    event_defaults = SoundEventDefaults(type="event type")
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "event type"


def test_get_sound_should_use_all_when_no_event_type_exists():

    all_details = SoundEventDefaults(type="all type")
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "all type"


def test_get_sound_should_not_include_type_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "type" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_print_correctly():

    all_details = SoundEventDefaults(type="all type")
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result: str = f"{defaults}"
    assert result == "{'all': {'type': 'all type'}, 'test.event': {'volume': 0.1}}"
