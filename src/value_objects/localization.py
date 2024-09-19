from pydantic import BaseModel, Field

from src import *

MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_ALTITUDE = -500
MAX_ALTITUDE = 9000


class Localization(BaseModel):
    latitude: float = Field(..., description="Latitude value", ge=MIN_LATITUDE, le=MAX_LATITUDE)
    longitude: float = Field(..., description="Longitude value", ge=MIN_LONGITUDE, le=MAX_LONGITUDE)
    altitude: float = Field(..., description="Altitude above sea level in meters", ge=MIN_ALTITUDE, le=MAX_ALTITUDE)

    def validate(self, latitude: float, longitude: float, altitude: float) -> Result[Success]:
        if not (MIN_LATITUDE <= latitude <= MAX_LATITUDE):
            return Result.failure(Error.validation(f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE}"))

        if not (MIN_LONGITUDE <= longitude <= MAX_LONGITUDE):
            return Result.failure(Error.validation(f"Longitude must be between {MIN_LONGITUDE} and {MAX_LONGITUDE}"))

        if not (MIN_ALTITUDE <= altitude <= MAX_ALTITUDE):
            return Result.failure(Error.validation(f"Altitude must be between {MIN_ALTITUDE} and {MAX_ALTITUDE}"))

        return Result.success()
