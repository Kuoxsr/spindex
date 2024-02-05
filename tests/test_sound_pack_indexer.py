
from sound_pack_indexer import get_combined_events
from sound_pack_indexer import Sound
from sound_pack_indexer import SoundEvent
import pytest


@pytest.fixture
def zero_events():
    return dict[str, SoundEvent]()


@pytest.fixture
def one_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/ambient/test01")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def different_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/death/test02")],
        subtitle="subtitles.entity.villager.death")

    events = dict[str, SoundEvent]()
    events["entity.villager.death"] = event

    return events


@pytest.fixture
def non_replacing_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=False,
        sounds=[Sound(name="namespace:entity/villager/ambient/test03")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def replace_not_specified_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        sounds=[Sound(name="namespace:entity/villager/ambient/test04")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def non_replacing_different_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=False,
        sounds=[Sound(name="namespace:entity/villager/hurt/test05")],
        subtitle="subtitles.entity.villager.hurt")

    events = dict[str, SoundEvent]()
    events["entity.villager.hurt"] = event

    return events


@pytest.fixture
def two_sounds_in_same_event() -> dict[str, SoundEvent]:

    sound1 = Sound(name="namespace:entity/villager/ambient/test10")
    sound2 = Sound(name="namespace:entity/villager/ambient/test20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def two_sounds_in_different_events() -> dict[str, SoundEvent]:

    sound1 = Sound(name="namespace:entity/villager/ambient/test10")
    sound2 = Sound(name="namespace:entity/villager/celebrate/test20")

    event1 = SoundEvent(
        replace=True,
        sounds=[sound1],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[sound2],
        subtitle="subtitles.entity.villager.celebrate")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event1
    events["entity.villager.celebrate"] = event2

    return events


def test_get_combined_events_empty_target_returns_source(one_event, zero_events):
    result = get_combined_events(one_event, zero_events)
    assert result == one_event


def test_get_combined_events_empty_source_returns_target(zero_events, one_event):
    result = get_combined_events(zero_events, one_event)
    assert result == one_event


def test_get_combined_events_name_collision(one_event):
    result = get_combined_events(one_event, one_event)
    assert result == one_event


def test_get_combined_events_one_source_two_targets_same_event(one_event, two_sounds_in_same_event):
    """
    Here we are making sure that when we add events with different names
    we actually get two sounds in the same namespace
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test10")
    sound3 = Sound(name="namespace:entity/villager/ambient/test20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2, sound3],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(one_event, two_sounds_in_same_event)
    assert result == expected


def test_get_combined_events_one_source_two_targets_different_events(one_event, two_sounds_in_different_events):
    """
    Here we are checking whether the incoming record is added to the correct
    event.  I'm not entirely sure that this is necessary.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test10")
    sound3 = Sound(name="namespace:entity/villager/celebrate/test20")

    event1 = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[sound3],
        subtitle="subtitles.entity.villager.celebrate")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.celebrate"] = event2

    # Call the function under test, and check the result
    result = get_combined_events(one_event, two_sounds_in_different_events)
    assert result == expected


def test_get_combined_events_different_events_no_similarities(one_event, different_event):
    """
    Here we are testing whether events are built correctly when there
    are no similarities at all between existing and incoming.
    """

    # Build expected combination
    event1 = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/ambient/test01")],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/death/test02")],
        subtitle="subtitles.entity.villager.death")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.death"] = event2

    # Call the function under test, and check the result
    result = get_combined_events(one_event, different_event)
    assert result == expected


def test_get_combined_events_sounds_should_be_sorted_by_name(two_sounds_in_same_event, one_event):
    """
    Here we are deliberately making the existing sounds *after* the incoming
    record to test whether it sorts the resulting list correctly or just adds
    the new sound to the bottom of the list.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test10")
    sound3 = Sound(name="namespace:entity/villager/ambient/test20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2, sound3],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(two_sounds_in_same_event, one_event)
    assert result == expected


def test_get_combined_events_should_not_add_replace_directive_to_existing_event_with_no_replace(
        one_event,
        replace_not_specified_event):
    """
    Here we are testing to make sure that an incoming record does not add a
    "replace" value to an event if one does not already exist for that event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test04")

    event = SoundEvent(
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(one_event, replace_not_specified_event)
    assert result == expected


def test_get_combined_events_should_not_remove_replace_directive(replace_not_specified_event, one_event):
    """
    Here we are testing whether the incoming record will remove a
    "replace": True value if the incoming record doesn't have one
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test04")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(replace_not_specified_event, one_event)
    assert result == expected


def test_get_combined_events_should_not_change_existing_replace_directive(one_event, non_replacing_event):
    """
    Here we are testing whether the incoming record will change the
    existing "replace": False value on the sound event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test01")
    sound2 = Sound(name="namespace:entity/villager/ambient/test03")

    event = SoundEvent(
        replace=False,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(one_event, non_replacing_event)
    assert result == expected


def test_get_combined_events_should_add_replace_directive_to_new_event(
        replace_not_specified_event,
        non_replacing_different_event):
    """
    Here we are testing to make sure that the incoming record will include
    a "replace" value when it is generating a new sound event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/test04")
    sound2 = Sound(name="namespace:entity/villager/hurt/test05")

    event1 = SoundEvent(
        sounds=[sound1],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=False,
        sounds=[sound2],
        subtitle="subtitles.entity.villager.hurt")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.hurt"] = event2

    # Call the function under test, and check the result
    result = get_combined_events(replace_not_specified_event, non_replacing_different_event)
    assert result == expected
