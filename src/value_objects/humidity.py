from pydantic import Field

from src import *
from value_object import ValueObject

MIN_HUMIDITY = 0
MAX_HUMIDITY = 100


class Humidity(ValueObject[float]):
    value: float = Field(..., description="Humidity value in percentage", ge=MIN_HUMIDITY, le=MAX_HUMIDITY)

    def validate(self, value: float) -> Result[Success]:
        if not (MIN_HUMIDITY <= value <= MAX_HUMIDITY):
            return Result.failure(Error.validation(f"Humidity must be between {MIN_HUMIDITY} and {MAX_HUMIDITY}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
