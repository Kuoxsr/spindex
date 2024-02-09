import json
from pathlib import Path

from objects.defaults import Defaults
from objects.typed_dictionaries import SoundEventDefaults
import pytest


def test_constructor_should_raise_typeerror_when_volume_not_float():

    event_defaults = SoundEventDefaults(volume="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_volume_less_than_zero():

    event_defaults = SoundEventDefaults(volume=-1)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_volume_greater_than_one():

    event_defaults = SoundEventDefaults(volume=1.1)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_pitch_not_float():

    event_defaults = SoundEventDefaults(pitch="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_weight_not_int():

    event_defaults = SoundEventDefaults(weight="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_weight_less_than_one():

    event_defaults = SoundEventDefaults(weight=0)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_weight_greater_than_32_bit_integer_limit():

    event_defaults = SoundEventDefaults(weight=2_147_483_648)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_stream_not_bool():

    event_defaults = SoundEventDefaults(stream="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_attenuation_distance_not_int():

    event_defaults = SoundEventDefaults(attenuation_distance="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_attenuation_distance_less_than_zero():

    event_defaults = SoundEventDefaults(attenuation_distance=-1)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_attenuation_distance_greater_than_32_bit_integer_limit():

    event_defaults = SoundEventDefaults(attenuation_distance=2_147_483_648)

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_preload_not_bool():

    event_defaults = SoundEventDefaults(preload="test")

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_typeerror_when_type_not_string():

    event_defaults = SoundEventDefaults(type=1)

    with pytest.raises(TypeError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_raise_valueerror_when_type_not_sound_or_event():

    event_defaults = SoundEventDefaults(type="test")

    with pytest.raises(ValueError):
        Defaults({"test.event": event_defaults})


def test_constructor_should_not_crash_if_data_is_empty():

    defaults = Defaults({})
    result = defaults.get_sound_event("test.event.name")
    assert result == dict({'sounds': [], 'subtitle': 'subtitles.test.event.name'})


# ------------------------------------------------------------------------


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


def test_get_sound_event_should_not_include_replace_if_none_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound_event("test.event")
    assert "replace" not in result.keys()

# ------------------------------------------------------------------------


def test_get_sound_event_should_return_empty_list_for_sounds():

    defaults = Defaults({"test.event": SoundEventDefaults()})

    result = defaults.get_sound_event("test.event")
    assert result["sounds"] == []

# ------------------------------------------------------------------------


def test_get_sound_event_should_use_event_subtitle():

    event_defaults = SoundEventDefaults(subtitle="subtitles.test.subtitle")
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
    event_defaults = SoundEventDefaults(volume=0.3)
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

    event_defaults = SoundEventDefaults(type="event")
    defaults = Defaults({"test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "event"


def test_get_sound_should_use_event_type_instead_of_all():

    all_details = SoundEventDefaults(type="sound")
    event_defaults = SoundEventDefaults(type="event")
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "event"


def test_get_sound_should_use_all_when_no_event_type_exists():

    all_details = SoundEventDefaults(type="sound")
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert result["type"] == "sound"


def test_get_sound_should_not_include_type_when_no_default_specified():

    all_defaults = SoundEventDefaults()
    defaults = Defaults({"all": all_defaults})

    result = defaults.get_sound("test.event", "test_sound_name")
    assert "type" not in result

# ------------------------------------------------------------------------


def test_get_sound_should_print_correctly():

    all_details = SoundEventDefaults(type="sound")
    event_defaults = SoundEventDefaults(volume=0.1)
    defaults = Defaults({"all": all_details, "test.event": event_defaults})

    result: str = f"{defaults}"
    assert result == "{'all': {'type': 'sound'}, 'test.event': {'volume': 0.1}}"

# ------------------------------------------------------------------------


def test_defaults_json_file_should_contain_all_these_properties():
    """
    This test was just to see if I constructed the json file correctly.
    I may not want to keep this hanging around, because every change to
    the file would cause a failure in this test.
    I guess I did discover an issue in defaults.py I needed to fix, so...
    not a total loss.  :shrug:
    """

    module_path = Path(__file__).parent.parent

    with open(module_path / 'defaults.json') as f:
        d = json.load(f)

    defaults = Defaults(d)

    enderman_scream = defaults.get_sound_event("entity.enderman.scream")
    assert len(enderman_scream.keys()) == 3
    assert enderman_scream["replace"] is True
    assert enderman_scream["sounds"] == []
    assert enderman_scream["subtitle"] == "subtitles.entity.enderman.ambient"

    enderman_sound = defaults.get_sound("entity.enderman.scream", "scream_sound")
    assert len(enderman_sound.keys()) == 1
    assert enderman_sound["name"] == "scream_sound"

    ghast_warn = defaults.get_sound_event("entity.ghast.warn")
    assert len(ghast_warn.keys()) == 3
    assert ghast_warn["replace"] is True
    assert ghast_warn["sounds"] == []
    assert ghast_warn["subtitle"] == "subtitles.entity.ghast.shoot"

    ghast_sound = defaults.get_sound("entity.ghast.warn", "ghast_test")
    assert len(ghast_sound.keys()) == 1
    assert ghast_sound["name"] == "ghast_test"

    player_big_fall = defaults.get_sound_event("entity.player.big_fall")
    assert len(player_big_fall.keys()) == 3
    assert player_big_fall["replace"] is True
    assert player_big_fall["sounds"] == []
    assert player_big_fall["subtitle"] == "subtitles.entity.generic.big_fall"

    player_big_fall_sound = defaults.get_sound("entity.player.big_fall", "player_big_fall_test")
    assert len(player_big_fall_sound.keys()) == 1
    assert player_big_fall_sound["name"] == "player_big_fall_test"

    player_small_fall = defaults.get_sound_event("entity.player.small_fall")
    assert len(player_small_fall.keys()) == 3
    assert player_small_fall["replace"] is True
    assert player_small_fall["sounds"] == []
    assert player_small_fall["subtitle"] == "subtitles.entity.generic.small_fall"

    player_small_fall_sound = defaults.get_sound("entity.player.small_fall", "player_small_fall_test")
    assert len(player_small_fall_sound.keys()) == 1
    assert player_small_fall_sound["name"] == "player_small_fall_test"

    villager_ambient = defaults.get_sound_event("entity.villager.ambient")
    assert len(villager_ambient.keys()) == 3
    assert villager_ambient["replace"] is True
    assert villager_ambient["sounds"] == []
    assert villager_ambient["subtitle"] == "subtitles.entity.villager.ambient"

    villager_ambient_sound = defaults.get_sound("entity.villager.ambient", "villager_ambient")
    assert len(villager_ambient_sound.keys()) == 2
    assert villager_ambient_sound["name"] == "villager_ambient"
    assert villager_ambient_sound["volume"] == 0.3

    villager_celebrate = defaults.get_sound_event("entity.villager.celebrate")
    assert len(villager_celebrate.keys()) == 3
    assert villager_celebrate["replace"] is True
    assert villager_celebrate["sounds"] == []
    assert villager_celebrate["subtitle"] == "subtitles.entity.villager.celebrate"

    villager_celebrate_sound = defaults.get_sound("entity.villager.celebrate", "villager_celebrate")
    assert len(villager_celebrate_sound.keys()) == 2
    assert villager_celebrate_sound["name"] == "villager_celebrate"
    assert villager_celebrate_sound["volume"] == 0.5

    villager_death = defaults.get_sound_event("entity.villager.death")
    assert len(villager_death.keys()) == 3
    assert villager_death["replace"] is True
    assert villager_death["sounds"] == []
    assert villager_death["subtitle"] == "subtitles.entity.villager.death"

    villager_death_sound = defaults.get_sound("entity.villager.death", "villager_death")
    assert len(villager_death_sound.keys()) == 2
    assert villager_death_sound["name"] == "villager_death"
    assert villager_death_sound["volume"] == 0.5

    villager_hurt = defaults.get_sound_event("entity.villager.hurt")
    assert len(villager_hurt.keys()) == 3
    assert villager_hurt["replace"] is True
    assert villager_hurt["sounds"] == []
    assert villager_hurt["subtitle"] == "subtitles.entity.villager.hurt"

    villager_hurt_sound = defaults.get_sound("entity.villager.hurt", "villager_hurt")
    assert len(villager_hurt_sound.keys()) == 2
    assert villager_hurt_sound["name"] == "villager_hurt"
    assert villager_hurt_sound["volume"] == 0.5

    villager_no = defaults.get_sound_event("entity.villager.no")
    assert len(villager_no.keys()) == 3
    assert villager_no["replace"] is True
    assert villager_no["sounds"] == []
    assert villager_no["subtitle"] == "subtitles.entity.villager.no"

    villager_no_sound = defaults.get_sound("entity.villager.no", "villager_no")
    assert len(villager_no_sound.keys()) == 2
    assert villager_no_sound["name"] == "villager_no"
    assert villager_no_sound["volume"] == 0.5

    villager_trade = defaults.get_sound_event("entity.villager.trade")
    assert len(villager_trade.keys()) == 3
    assert villager_trade["replace"] is True
    assert villager_trade["sounds"] == []
    assert villager_trade["subtitle"] == "subtitles.entity.villager.trade"

    villager_trade_sound = defaults.get_sound("entity.villager.trade", "villager_trade")
    assert len(villager_trade_sound.keys()) == 2
    assert villager_trade_sound["name"] == "villager_trade"
    assert villager_trade_sound["volume"] == 0.5

    villager_yes = defaults.get_sound_event("entity.villager.yes")
    assert len(villager_yes.keys()) == 3
    assert villager_yes["replace"] is True
    assert villager_yes["sounds"] == []
    assert villager_yes["subtitle"] == "subtitles.entity.villager.yes"

    villager_yes_sound = defaults.get_sound("entity.villager.yes", "villager_yes")
    assert len(villager_yes_sound.keys()) == 2
    assert villager_yes_sound["name"] == "villager_yes"
    assert villager_yes_sound["volume"] == 0.5

    witch_ambient = defaults.get_sound_event("entity.witch.ambient")
    assert len(witch_ambient.keys()) == 3
    assert witch_ambient["replace"] is True
    assert witch_ambient["sounds"] == []
    assert witch_ambient["subtitle"] == "subtitles.entity.witch.ambient"

    witch_ambient_sound = defaults.get_sound("entity.witch.ambient", "witch_ambient")
    assert len(witch_ambient_sound.keys()) == 2
    assert witch_ambient_sound["name"] == "witch_ambient"
    assert witch_ambient_sound["volume"] == 0.7

    witch_celebrate = defaults.get_sound_event("entity.witch.celebrate")
    assert len(witch_celebrate.keys()) == 3
    assert witch_celebrate["replace"] is True
    assert witch_celebrate["sounds"] == []
    assert witch_celebrate["subtitle"] == "subtitles.entity.witch.celebrate"

    witch_celebrate_sound = defaults.get_sound("entity.witch.celebrate", "witch_celebrate")
    assert len(witch_celebrate_sound.keys()) == 2
    assert witch_celebrate_sound["name"] == "witch_celebrate"
    assert witch_celebrate_sound["volume"] == 0.7

    witch_death = defaults.get_sound_event("entity.witch.death")
    assert len(witch_death.keys()) == 3
    assert witch_death["replace"] is True
    assert witch_death["sounds"] == []
    assert witch_death["subtitle"] == "subtitles.entity.witch.death"

    witch_death_sound = defaults.get_sound("entity.witch.death", "witch_death")
    assert len(witch_death_sound.keys()) == 2
    assert witch_death_sound["name"] == "witch_death"
    assert witch_death_sound["volume"] == 0.7

    assert True

