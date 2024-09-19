from pydantic import Field

from src import *
from value_object import ValueObject

MIN_VIBRATION = 0
MAX_VIBRATION = 1000


class Vibration(ValueObject[float]):
    value: float = Field(..., description="Vibration value in Hz", ge=MIN_VIBRATION, le=MAX_VIBRATION)

    def validate(self, value: float) -> Result[Success]:
        if not (MIN_VIBRATION <= value <= MAX_VIBRATION):
            return Result.failure(Error.validation(f"Vibration must be between {MIN_VIBRATION} and {MAX_VIBRATION}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
