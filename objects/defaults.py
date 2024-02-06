
from objects.typed_dictionaries import SoundEventDefaults, SoundEvent, Sound


class Defaults:
    def __init__(self, data: dict[str, SoundEventDefaults]):
        self.data: dict[str, SoundEventDefaults] = data

    def __repr__(self):
        print(f"{self.data}")

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

        a: SoundEventDefaults = self.data["all"]
        d: SoundEventDefaults = self.data[event_name]

        default_volume = d["volume"] if d["volume"] else a["volume"] if a["volume"] else None
        default_pitch = d["pitch"] if d["pitch"] else a["pitch"] if a["pitch"] else None
        default_weight = d["weight"] if d["weight"] else a["weight"] if a["weight"] else None
        default_stream = d["stream"] if d["stream"] else a["stream"] if a["stream"] else None
        default_attenuation = \
            d["attenuation_distance"] if \
            d["attenuation_distance"] else \
            a["attenuation_distance"] if \
            a["attenuation_distance"] else None
        default_preload = d["preload"] if d["preload"] else a["preload"] if a["preload"] else None
        default_type = d["type"] if d["type"] else a["type"] if a["type"] else None

        sound: Sound = Sound(name=sound_name)
        sound.volume = default_volume
        sound.pitch = default_pitch
        sound.weight = default_weight
        sound.stream = default_stream
        sound.attenuation_distance = default_attenuation
        sound.preload = default_preload
        sound.type = default_type

        return sound

