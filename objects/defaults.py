
from enum import Enum
from objects.typed_dictionaries import SoundEventDefaults, SoundEvent, Sound


class Defaults:
    def __init__(self, data: dict[str, SoundEventDefaults]):

        if self.__validate_data(data):
            self.data: dict[str, SoundEventDefaults] = data

    def __str__(self):
        return f"{self.data}"

    @staticmethod
    def __validate_data(data: dict[str, SoundEventDefaults]):

        for key, value in data.items():

            if "volume" in value:

                if type(value["volume"]) is not float and type(value["volume"]) is not int:
                    raise TypeError("volume must be a float datatype between 0.0 and 1.0")

                if value["volume"] < 0.0:
                    raise ValueError("volume cannot be less than zero")

                if value["volume"] > 1.0:
                    raise ValueError("volume cannot be greater than 1.0")

            if "pitch" in value:

                if type(value["pitch"]) is not float and type(value["pitch"]) is not int:
                    raise TypeError("pitch must be a float datatype")

            if "weight" in value:

                if type(value["weight"]) is not int:
                    raise TypeError("weight must be an integer between 1 and 2,147,483,647")

                if value["weight"] < 1:
                    raise ValueError("weight cannot be less than 1")

                if value["weight"] > 2_147_483_647:
                    raise ValueError("weight cannot be greater than 2,147,483,647")

            if "stream" in value and type(value["stream"]) is not bool:
                raise TypeError("stream must be a boolean datatype")

            if "attenuation_distance" in value:

                if type(value["attenuation_distance"]) is not int:
                    raise TypeError("attenuation_distance must be an integer between 0 and 2,147,483,647")

                if value["attenuation_distance"] < 0:
                    raise ValueError("attenuation_distance cannot be less than zero")

                if value["attenuation_distance"] > 2_147_483_647:
                    raise ValueError("attenuation_distance cannot be greater than 2,147,483,647")

            if "preload" in value and type(value["preload"]) is not bool:
                raise TypeError("preload must be a boolean datatype")

            if "type" in value:

                if type(value["type"]) is not str:
                    raise TypeError("type must be a string containing either 'sound' or 'event'")

                if value["type"] != "sound" and value["type"] != "event":
                    raise ValueError("type must be either 'sound' or 'event'")

        return True

    def get_sound_event(self, event_name: str):

        a: SoundEventDefaults = self.data["all"] if "all" in self.data else SoundEventDefaults()
        d: SoundEventDefaults = self.data[event_name] if event_name in self.data else SoundEventDefaults()

        default_replace = d["replace"] if "replace" in d else a["replace"] if "replace" in a else None

        # Build subtitle from default if one exists, otherwise use event_name
        subtitle: str = d["subtitle"] if "subtitle" in d else f"subtitles.{event_name}"

        event: SoundEvent = SoundEvent(
            sounds=[],
            subtitle=subtitle)

        if default_replace is not None:
            event["replace"] = default_replace

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

