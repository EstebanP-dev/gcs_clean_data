from pydantic import Field

from src import *
from value_object import ValueObject

MIN_SOUND_LEVEL = 0
MAX_SOUND_LEVEL = 100


class SoundLevel(ValueObject[float]):
    value: float = Field(..., description="Sound level value in dB", ge=MIN_SOUND_LEVEL, le=MAX_SOUND_LEVEL)

    def validate(self, value: float) -> Result[Success]:
        if not (MIN_SOUND_LEVEL <= value <= MAX_SOUND_LEVEL):
            return Result.failure(Error.validation(f"Sound level must be between {MIN_SOUND_LEVEL} and {MAX_SOUND_LEVEL}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
