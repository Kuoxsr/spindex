
from typing import TypedDict, NotRequired


class Sound(TypedDict):
    name: str
    volume: NotRequired[float]
    pitch: NotRequired[float]
    weight: NotRequired[int]
    stream: NotRequired[bool]
    attenuation_distance: NotRequired[int]
    preload: NotRequired[bool]
    type: NotRequired[str]


class SoundEvent(TypedDict):
    replace: NotRequired[bool]
    sounds: list[Sound]
    subtitle: NotRequired[str]


# This class holds default values for sound events
class SoundEventDefaults(TypedDict):
    replace: NotRequired[bool]
    subtitle: NotRequired[str]
    volume: NotRequired[float]
    weight: NotRequired[int]
    pitch: NotRequired[float]
    stream: NotRequired[bool]
    attenuation_distance: NotRequired[int]
    preload: NotRequired[bool]
    type: NotRequired[str]

