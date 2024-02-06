
from objects.typed_dictionaries import SoundEventDefaults, SoundEvent, Sound


class Defaults:
    def __init__(self, data: dict[str, SoundEventDefaults]):
        self.data: dict[str, SoundEventDefaults] = data

    def __str__(self):
        return f"{self.data}"

    def get_sound_event(self, event_name: str):

        a: SoundEventDefaults = self.data["all"] if "all" in self.data else SoundEventDefaults()
        d: SoundEventDefaults = self.data[event_name] if event_name in self.data else SoundEventDefaults()

        default_replace = d["replace"] if "replace" in d else a["replace"] if "replace" in a else True

        # Build subtitle from default if one exists, otherwise use event_name
        subtitle: str = f'subtitles.{d["subtitle"] if "subtitle" in d else event_name}'

        event: SoundEvent = SoundEvent(
            replace=default_replace,
            sounds=[],
            subtitle=subtitle)

        return event

    def get_sound(self, event_name, sound_name):

        a: SoundEventDefaults = self.data["all"] if "all" in self.data else SoundEventDefaults()
        d: SoundEventDefaults = self.data[event_name] if event_name in self.data else SoundEventDefaults()

        default_volume = d["volume"] if "volume" in d else a["volume"] if "volume" in a else None
        default_weight = d["weight"] if "weight" in d else a["weight"] if "weight" in a else None
        default_pitch = d["pitch"] if "pitch" in d else a["pitch"] if "pitch" in a else None
        default_stream = d["stream"] if "stream" in d else a["stream"] if "stream" in a else None
        default_attenuation = \
            d["attenuation_distance"] if "attenuation_distance" in d else \
            a["attenuation_distance"] if "attenuation_distance" in a else None
        default_preload = d["preload"] if "preload" in d else a["preload"] if "preload" in a else None
        default_type = d["type"] if "type" in d else a["type"] if "type" in a else None

        sound: Sound = Sound(name=sound_name)

        if default_volume is not None:
            sound["volume"] = default_volume

        if default_weight is not None:
            sound["weight"] = default_weight

        if default_pitch is not None:
            sound["pitch"] = default_pitch

        if default_stream is not None:
            sound["stream"] = default_stream

        if default_attenuation is not None:
            sound["attenuation_distance"] = default_attenuation

        if default_preload is not None:
            sound["preload"] = default_preload

        if default_type is not None:
            sound["type"] = default_type

        return sound

