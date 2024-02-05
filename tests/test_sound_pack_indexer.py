
from sound_pack_indexer import get_combined_events
from sound_pack_indexer import Sound
from sound_pack_indexer import SoundEvent
import pytest


@pytest.fixture
def zero_events():
    return dict[str, SoundEvent]()


@pytest.fixture
def ambient_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/ambient/ambient")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def death_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/death/death")],
        subtitle="subtitles.entity.villager.death")

    events = dict[str, SoundEvent]()
    events["entity.villager.death"] = event

    return events


@pytest.fixture
def non_replacing_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=False,
        sounds=[Sound(name="namespace:entity/villager/ambient/non-replacing")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def replace_not_specified_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        sounds=[Sound(name="namespace:entity/villager/ambient/ambient_replace-not-specified")],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def hurt_event_non_replacing() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=False,
        sounds=[Sound(name="namespace:entity/villager/hurt/hurt-non-replacing")],
        subtitle="subtitles.entity.villager.hurt")

    events = dict[str, SoundEvent]()
    events["entity.villager.hurt"] = event

    return events


@pytest.fixture
def two_sounds_in_same_event() -> dict[str, SoundEvent]:

    sound1 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event

    return events


@pytest.fixture
def two_sounds_in_different_events() -> dict[str, SoundEvent]:

    sound1 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound2 = Sound(name="namespace:entity/villager/yes/yes20")

    event1 = SoundEvent(
        replace=True,
        sounds=[sound1],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[sound2],
        subtitle="subtitles.entity.villager.yes")

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event1
    events["entity.villager.yes"] = event2

    return events


def test_get_combined_events_empty_target_returns_source(ambient_event, zero_events):
    result = get_combined_events(ambient_event, zero_events)
    assert result == ambient_event


def test_get_combined_events_empty_source_returns_target(zero_events, ambient_event):
    result = get_combined_events(zero_events, ambient_event)
    assert result == ambient_event


def test_get_combined_events_name_collision(ambient_event):
    result = get_combined_events(ambient_event, ambient_event)
    assert result == ambient_event


def test_get_combined_events_one_source_two_targets_same_event(ambient_event, two_sounds_in_same_event):
    """
    Here we are making sure that when we add events with different names
    we actually get two sounds in the same namespace
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound3 = Sound(name="namespace:entity/villager/ambient/ambient20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2, sound3],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(ambient_event, two_sounds_in_same_event)
    assert result == expected


def test_get_combined_events_one_source_two_targets_different_events(ambient_event, two_sounds_in_different_events):
    """
    Here we are checking whether the incoming record is added to the correct
    event.  I'm not entirely sure that this is necessary.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound3 = Sound(name="namespace:entity/villager/yes/yes20")

    event1 = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[sound3],
        subtitle="subtitles.entity.villager.yes")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.yes"] = event2

    # Call the function under test, and check the result
    result = get_combined_events(ambient_event, two_sounds_in_different_events)
    assert result == expected


def test_get_combined_events_different_events_no_similarities(ambient_event, death_event):
    """
    Here we are testing whether events are built correctly when there
    are no similarities at all between existing and incoming.
    """

    # Build expected combination
    event1 = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/ambient/ambient")],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[Sound(name="namespace:entity/villager/death/death")],
        subtitle="subtitles.entity.villager.death")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.death"] = event2

    # Call the function under test, and check the result
    result = get_combined_events(ambient_event, death_event)
    assert result == expected


def test_get_combined_events_sounds_should_be_sorted_by_name(two_sounds_in_same_event, ambient_event):
    """
    Here we are deliberately making the existing sounds *after* the incoming
    record to test whether it sorts the resulting list correctly or just adds
    the new sound to the bottom of the list.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound3 = Sound(name="namespace:entity/villager/ambient/ambient20")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2, sound3],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(two_sounds_in_same_event, ambient_event)
    assert result == expected


def test_get_combined_events_should_sort_events_by_event_name(death_event, two_sounds_in_different_events):
    """
    This test is to make sure that the entire dictionary is being sorted by
    event name.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound2 = Sound(name="namespace:entity/villager/death/death")
    sound3 = Sound(name="namespace:entity/villager/yes/yes20")

    event1 = SoundEvent(
        replace=True,
        sounds=[sound1],
        subtitle="subtitles.entity.villager.ambient")

    event2 = SoundEvent(
        replace=True,
        sounds=[sound2],
        subtitle="subtitles.entity.villager.death")

    event3 = SoundEvent(
        replace=True,
        sounds=[sound3],
        subtitle="subtitles.entity.villager.yes")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event1
    expected["entity.villager.death"] = event2
    expected["entity.villager.yes"] = event3

    # Call the function under test, and check the result
    result = get_combined_events(death_event, two_sounds_in_different_events)
    assert result == expected


def test_get_combined_events_should_not_add_replace_directive_to_existing_event_with_no_replace(
        ambient_event,
        replace_not_specified_event):
    """
    Here we are testing to make sure that an incoming record does not add a
    "replace" value to an event if one does not already exist for that event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient_replace-not-specified")

    event = SoundEvent(
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(ambient_event, replace_not_specified_event)
    assert result == expected


def test_get_combined_events_should_not_remove_replace_directive(replace_not_specified_event, ambient_event):
    """
    Here we are testing whether the incoming record will remove a
    "replace": True value if the incoming record doesn't have one
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/ambient_replace-not-specified")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(replace_not_specified_event, ambient_event)
    assert result == expected


def test_get_combined_events_should_not_change_existing_replace_directive(ambient_event, non_replacing_event):
    """
    Here we are testing whether the incoming record will change the
    existing "replace": False value on the sound event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient")
    sound2 = Sound(name="namespace:entity/villager/ambient/non-replacing")

    event = SoundEvent(
        replace=False,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.ambient")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.ambient"] = event

    # Call the function under test, and check the result
    result = get_combined_events(ambient_event, non_replacing_event)
    assert result == expected


def test_get_combined_events_should_add_replace_directive_to_new_event(
        replace_not_specified_event,
        hurt_event_non_replacing):
    """
    Here we are testing to make sure that the incoming record will include
    a "replace" value when it is generating a new sound event
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/ambient/ambient_replace-not-specified")
    sound2 = Sound(name="namespace:entity/villager/hurt/hurt-non-replacing")

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
    result = get_combined_events(replace_not_specified_event, hurt_event_non_replacing)
    assert result == expected
