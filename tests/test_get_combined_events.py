import pytest

from spindex import get_combined_events
from typed_dictionaries import SoundEvent, Sound


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
def death_event_disordered() -> dict[str, SoundEvent]:

    event = SoundEvent(
        sounds=[Sound(name="namespace:entity/villager/death/death")],
        replace=True,
        subtitle="subtitles.entity.villager.death")

    events = dict[str, SoundEvent]()
    events["entity.villager.death"] = event

    return events


@pytest.fixture
def trade_event() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name=f"namespace:entity/villager/trade/trade")],
        subtitle="subtitles.entity.villager.trade")

    events = dict[str, SoundEvent]()
    events["entity.villager.trade"] = event
    return events


@pytest.fixture
def trade_event_no_subtitle() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name=f"namespace:entity/villager/trade/trade-no-subtitle")])

    events = dict[str, SoundEvent]()
    events["entity.villager.trade"] = event
    return events


@pytest.fixture
def trade_event_bad_subtitle() -> dict[str, SoundEvent]:

    event = SoundEvent(
        replace=True,
        sounds=[Sound(name=f"namespace:entity/villager/trade/trade-bad-subtitle")],
        subtitle="this is not the correct subtitle")

    events = dict[str, SoundEvent]()
    events["entity.villager.trade"] = event
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


@pytest.fixture
def two_sounds_in_different_events_disordered() -> dict[str, SoundEvent]:

    sound1 = Sound(name="namespace:entity/villager/ambient/ambient10")
    sound2 = Sound(name="namespace:entity/villager/yes/yes20")

    event1 = SoundEvent(
        sounds=[sound1],
        subtitle="subtitles.entity.villager.ambient",
        replace=True)

    event2 = SoundEvent(
        subtitle="subtitles.entity.villager.yes",
        replace=True,
        sounds=[sound2])

    events = dict[str, SoundEvent]()
    events["entity.villager.ambient"] = event1
    events["entity.villager.yes"] = event2

    return events


def test_get_combined_events_should_return_incoming_when_existing_is_empty(ambient_event, zero_events):
    result = get_combined_events(ambient_event, zero_events)
    assert result == ambient_event


def test_get_combined_events_should_return_existing_when_incoming_is_empty(zero_events, ambient_event):
    result = get_combined_events(zero_events, ambient_event)
    assert result == ambient_event


def test_get_combined_events_should_not_duplicate_sounds_that_already_exist(ambient_event):
    result = get_combined_events(ambient_event, ambient_event)
    assert result == ambient_event


def test_get_combined_events_should_add_sounds_to_existing_event(ambient_event, two_sounds_in_same_event):
    """
    Here we are making sure that when we add events with different names
    we actually get multiple sounds in the same namespace
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


def test_get_combined_events_should_add_sounds_to_correct_event(
        ambient_event,
        two_sounds_in_different_events):
    """
    Here we are checking whether the incoming record is added to the correct event.
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


def test_get_combined_events_should_add_new_events(ambient_event, death_event):
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
    assert str(result) == str(expected)


def test_get_combined_events_should_sort_replace_sounds_subtitle_in_correct_order(
        death_event_disordered,
        two_sounds_in_different_events_disordered):
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
    result = get_combined_events(
        death_event_disordered,
        two_sounds_in_different_events_disordered)

    assert str(result) == str(expected)


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


def test_get_combined_events_should_add_subtitle_if_none_exists(trade_event, trade_event_no_subtitle):
    """
    This test makes sure that if no subtitle exists, one should be added
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/trade/trade")
    sound2 = Sound(name="namespace:entity/villager/trade/trade-no-subtitle")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.trade")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.trade"] = event

    # Call the function under test, and check the result
    result = get_combined_events(trade_event, trade_event_no_subtitle)
    assert result == expected


def test_get_combined_events_should_not_remove_subtitle_if_one_exists(trade_event_no_subtitle, trade_event):
    """
    This test makes sure that if an incoming record has no subtitle, it doesn't remove the existing
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/trade/trade")
    sound2 = Sound(name="namespace:entity/villager/trade/trade-no-subtitle")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.trade")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.trade"] = event

    # Call the function under test, and check the result
    result = get_combined_events(trade_event_no_subtitle, trade_event)
    assert result == expected


def test_get_combined_events_should_not_change_existing_subtitle(trade_event_bad_subtitle, trade_event):
    """
    This test makes sure that if an incoming record has a different subtitle,
    that it doesn't replace the existing subtitle.
    """

    # Build expected combination
    sound1 = Sound(name="namespace:entity/villager/trade/trade")
    sound2 = Sound(name="namespace:entity/villager/trade/trade-bad-subtitle")

    event = SoundEvent(
        replace=True,
        sounds=[sound1, sound2],
        subtitle="subtitles.entity.villager.trade")

    expected = dict[str, SoundEvent]()
    expected["entity.villager.trade"] = event

    # Call the function under test, and check the result
    result = get_combined_events(trade_event_bad_subtitle, trade_event)
    assert result == expected
