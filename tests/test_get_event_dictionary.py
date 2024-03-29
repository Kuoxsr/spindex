
import pytest

from pathlib import Path
from spindex import get_event_dictionary


def test_get_event_dictionary_should_return_empty_object_when_file_does_not_exist():

    path: Path = Path("/test/path/to/sounds.json")

    result = get_event_dictionary(path)
    assert result == {}


@pytest.mark.parametrize(
    "file_path, file_contents, expectation", [
        ("/test/path/to/sounds.json", None, {}),

        ("/test/path/to/sounds.json",
         '{"test.event":{"sounds":["path/to/sound"]}}',
         {'test.event': {'sounds': ['path/to/sound']}})
    ])
def test_get_event_dictionary_should_return_empty_object_when_file_has_no_contents(
        fs, file_path, file_contents, expectation):

    fs.create_file(file_path, contents=file_contents)
    path: Path = Path(file_path)

    result = get_event_dictionary(path)
    assert result == expectation


@pytest.mark.parametrize(
    "file_path, file_contents, expectation", [
        ("/test/path/to/sounds.json",
         '{"test.event":{"sounds":["path/to/sound"]}}',
         {'test.event': {'sounds': ['path/to/sound']}}),

        ("/another/test/generated_sounds.json",
         '{"second.test":{"sounds":[{"name": "namespace:path/to/other_sound"}]}}',
         {"second.test": {"sounds": [{"name": "namespace:path/to/other_sound"}]}})
    ])
def test_get_event_dictionary_should_return_dictionary_representation_of_file_contents(
        fs, file_path, file_contents, expectation):

    fs.create_file(file_path, contents=file_contents)
    path: Path = Path(file_path)

    result = get_event_dictionary(path)
    assert result == expectation
