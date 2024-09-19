from pydantic import Field

from src import *
from value_object import ValueObject

MIN_BATTERY_LEVEL = 0
MAX_BATTERY_LEVEL = 100


class BatteryLevel(ValueObject[float]):
    value: float = Field(..., description="Battery level in percentage", ge=MIN_BATTERY_LEVEL, le=MAX_BATTERY_LEVEL)

    def validate(self, value: float) -> Result[Success]:
        if not (MIN_BATTERY_LEVEL <= value <= MAX_BATTERY_LEVEL):
            return Result.failure(
                Error.validation(f"Battery level must be between {MIN_BATTERY_LEVEL} and {MAX_BATTERY_LEVEL}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
