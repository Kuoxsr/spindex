from pathlib import Path

from sound_pack_indexer import get_event_name


def test_get_event_name_should_return_empty_string_if_name_too_short():

    # Arrange
    file: Path = Path("/villager/ambient/filename.ogg")

    # Act
    result = get_event_name(file)

    # Assert
    assert result == ""


def test_get_event_name_should_find_three_segment_name_at_index_one():

    # Arrange
    file: Path = Path("/entity/villager/ambient/filename.ogg")

    # Act
    result = get_event_name(file)

    # Assert
    assert result == "entity.villager.ambient"


def test_get_event_name_should_find_three_segment_name_at_index_two():

    # Arrange
    file: Path = Path("team-member/entity/witch/ambient/filename.ogg")

    # Act
    result = get_event_name(file)

    # Assert
    assert result == "entity.witch.ambient"


def test_get_event_name_should_find_two_segment_name_at_index_one():

    # Arrange
    file: Path = Path("/music_disc/blocks/filename.ogg")

    # Act
    result = get_event_name(file)

    # Assert
    assert result == "music_disc.blocks"


def test_get_event_name_should_find_two_segment_name_at_index_two():

    # Arrange
    file: Path = Path("team-member/weather/rain/filename.ogg")

    # Act
    result = get_event_name(file)

    # Assert
    assert result == "weather.rain"

