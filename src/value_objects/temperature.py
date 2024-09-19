from pydantic import Field

from src import *
from value_object import ValueObject

MIN_TEMPERATURE = -100
MAX_TEMPERATURE = 100


class Temperature(ValueObject[float]):
    value: float = Field(..., description="Temperature value in Celsius", ge=MIN_TEMPERATURE, le=MAX_TEMPERATURE)

    def validate(self, value: float) -> Result[Success]:
        if not (MIN_TEMPERATURE <= value <= MAX_TEMPERATURE):
            return Result.failure(Error.validation(f"Temperature must be between {MIN_TEMPERATURE} and {MAX_TEMPERATURE}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
