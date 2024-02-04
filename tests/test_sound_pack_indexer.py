
from sound_pack_indexer import get_combined_events
from sound_pack_indexer import Sound
from sound_pack_indexer import SoundEvent
import pytest


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
def zero_events():
    return dict[str, SoundEvent]()


def test_get_combined_events_empty_target_returns_source(one_event, zero_events):
    result = get_combined_events(one_event, zero_events)
    assert result == one_event


def test_get_combined_events_empty_source_returns_target(zero_events, one_event):
    result = get_combined_events(zero_events, one_event)
    assert result == one_event

