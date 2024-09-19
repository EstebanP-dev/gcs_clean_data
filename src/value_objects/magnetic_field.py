from pydantic import BaseModel, Field

from src import *

MIN_MAGNETIC_FIELD = -1000
MAX_MAGNETIC_FIELD = 1000


class MagneticField(BaseModel):
    value_x: float = Field(..., description="Magnetic field value in Gauss", ge=MIN_MAGNETIC_FIELD,
                           le=MAX_MAGNETIC_FIELD)
    value_y: float = Field(..., description="Magnetic field value in Gauss", ge=MIN_MAGNETIC_FIELD,
                           le=MAX_MAGNETIC_FIELD)
    value_z: float = Field(..., description="Magnetic field value in Gauss", ge=MIN_MAGNETIC_FIELD,
                           le=MAX_MAGNETIC_FIELD)

    def validate(self, value_x: float, value_y: float, value_z: float) -> Result[Success]:
        if not (MIN_MAGNETIC_FIELD <= value_x <= MAX_MAGNETIC_FIELD):
            return Result.failure(
                Error.validation(f"Magnetic field X must be between {MIN_MAGNETIC_FIELD} and {MAX_MAGNETIC_FIELD}"))

        if not (MIN_MAGNETIC_FIELD <= value_y <= MAX_MAGNETIC_FIELD):
            return Result.failure(
                Error.validation(f"Magnetic field Y must be between {MIN_MAGNETIC_FIELD} and {MAX_MAGNETIC_FIELD}"))

        if not (MIN_MAGNETIC_FIELD <= value_z <= MAX_MAGNETIC_FIELD):
            return Result.failure(
                Error.validation(f"Magnetic field Z must be between {MIN_MAGNETIC_FIELD} and {MAX_MAGNETIC_FIELD}"))

        return Result.success()

    def equals(self, other: float) -> bool:
        return self.value == other
