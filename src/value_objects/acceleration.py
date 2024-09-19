from pydantic import BaseModel, Field

from src import *

MIN_ACCELERATION = 0
MAX_ACCELERATION = 100


class Acceleration(BaseModel):
    value_x: float = Field(..., description="Acceleration value in m/s^2", ge=MIN_ACCELERATION, le=MAX_ACCELERATION)
    value_y: float = Field(..., description="Acceleration value in m/s^2", ge=MIN_ACCELERATION, le=MAX_ACCELERATION)
    value_z: float = Field(..., description="Acceleration value in m/s^2", ge=MIN_ACCELERATION, le=MAX_ACCELERATION)

    def validate(self, value_x: float, value_y: float, value_z: float) -> Result[Success]:
        if not (MIN_ACCELERATION <= value_x <= MAX_ACCELERATION):
            return Result.failure(Error.validation(f"Acceleration X must be between {MIN_ACCELERATION} and {MAX_ACCELERATION}"))

        if not (MIN_ACCELERATION <= value_y <= MAX_ACCELERATION):
            return Result.failure(Error.validation(f"Acceleration Y must be between {MIN_ACCELERATION} and {MAX_ACCELERATION}"))

        if not (MIN_ACCELERATION <= value_z <= MAX_ACCELERATION):
            return Result.failure(Error.validation(f"Acceleration Z must be between {MIN_ACCELERATION} and {MAX_ACCELERATION}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
