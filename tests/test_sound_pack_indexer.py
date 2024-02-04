
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

    # Call the function under test
    result = get_combined_events(one_event, two_sounds_in_same_event)

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

    assert result == expected


def test_get_combined_events_one_source_two_targets_different_events(one_event, two_sounds_in_different_events):
    """
    Here we are checking whether the incoming record is added to the correct
    event.  I'm not entirely sure that this is necessary.
    """

    # Call the function under test
    result = get_combined_events(one_event, two_sounds_in_different_events)

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

    assert result == expected


def test_get_combined_events_different_events_no_similarities(one_event, different_event):
    """
    Here we are testing whether events are built correctly when there
    are no similarities at all between existing and incoming.
    """

    # Call the function under test
    result = get_combined_events(one_event, different_event)

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

    assert result == expected


def test_get_combined_events_results_should_be_sorted_by_name(two_sounds_in_same_event, one_event):
    """
    Here we are deliberately making the existing records *after* the incoming
    record to test whether it sorts the resulting list correctly or just adds
    the new record to the bottom of the list.
    """

    # Call the function under test
    result = get_combined_events(two_sounds_in_same_event, one_event)

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

    assert result == expected

