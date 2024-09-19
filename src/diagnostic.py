from typing_extensions import Self

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

from primitives import *


class Diagnostic(BaseModel):
    id: str = Field(..., description="ID único del sensor")
    device_id: str = Field(..., description="ID único del dispositivo")
    timestamp: datetime = Field(..., description="Fecha y hora en la que se registró el dato")
    temperature: Optional[float] = Field(None, description="Temperatura en grados Celsius", ge=-100, le=100)
    humidity: Optional[float] = Field(None, description="Humedad relativa en porcentaje", ge=0, le=100)
    acceleration_x: Optional[float] = Field(None, description="Aceleración en el eje X en m/s²", ge=-100, le=100)
    acceleration_y: Optional[float] = Field(None, description="Aceleración en el eje Y en m/s²", ge=-100, le=100)
    acceleration_z: Optional[float] = Field(None, description="Aceleración en el eje Z en m/s²", ge=-100, le=100)
    vibration: Optional[float] = Field(None, description="Vibración en mm/s", ge=0, le=1000)
    sound_level: Optional[float] = Field(None, description="Nivel de sonido en decibelios", ge=0, le=200)
    battery_level: Optional[float] = Field(None, description="Nivel de batería en porcentaje", ge=0, le=100)
    magnetic_field_x: Optional[float] = Field(None, description="Campo magnético en el eje X en microteslas", ge=-1000,
                                              le=1000)
    magnetic_field_y: Optional[float] = Field(None, description="Campo magnético en el eje Y en microteslas", ge=-1000,
                                              le=1000)
    magnetic_field_z: Optional[float] = Field(None, description="Campo magnético en el eje Z en microteslas", ge=-1000,
                                              le=1000)
    latitude: Optional[float] = Field(None, description="Latitud del sensor", ge=-90, le=90)
    longitude: Optional[float] = Field(None, description="Longitud del sensor", ge=-180, le=180)
    altitude: Optional[float] = Field(None, description="Altitud sobre el nivel del mar en metros", ge=-500, le=9000)

    def validate_temperature(self) -> Result[Success]:
        if self.temperature is None:
            return Result.failure(Error.validation("Temperature is required"))
        if not (-100 <= self.temperature <= 100):
            return Result.failure(Error.validation("Temperature must be between -100 and 100"))

        return Result.success()

    def validate_humidity(self) -> Result[Success]:
        if self.humidity is None:
            return Result.failure(Error.validation("Humidity is required"))

        if not (0 <= self.humidity <= 100):
            return Result.failure(Error.validation("Humidity must be between 0 and 100"))

        return Result.success()

    def validate_accelerations(self) -> Result[Success]:
        if self.acceleration_x is None or self.acceleration_y is None or self.acceleration_z is None:
            return Result.failure(Error.validation("Acceleration values are required"))

        if not (-100 <= self.acceleration_x <= 100):
            return Result.failure(Error.validation("Acceleration X must be between -100 and 100"))

        if not (-100 <= self.acceleration_y <= 100):
            return Result.failure(Error.validation("Acceleration Y must be between -100 and 100"))

        if not (-100 <= self.acceleration_z <= 100):
            return Result.failure(Error.validation("Acceleration Z must be between -100 and 100"))

        return Result.success()

    def validate_vibration(self) -> Result[Success]:
        if self.vibration is None:
            return Result.failure(Error.validation("Vibration is required"))

        if not (0 <= self.vibration <= 1000):
            return Result.failure(Error.validation("Vibration must be between 0 and 1000"))

        return Result.success()

    def validate_sound_level(self) -> Result[Success]:
        if self.sound_level is None:
            return Result.failure(Error.validation("Sound level is required"))

        if not (0 <= self.sound_level <= 200):
            return Result.failure(Error.validation("Sound level must be between 0 and 200"))

        return Result.success()

    def validate_battery_level(self) -> Result[Success]:
        if self.battery_level is None:
            return Result.failure(Error.validation("Battery level is required"))

        if not (0 <= self.battery_level <= 100):
            return Result.failure(Error.validation("Battery level must be between 0 and 100"))

        return Result.success()

    def validate_magnetic_fields(self) -> Result[Success]:
        if self.magnetic_field_x is None or self.magnetic_field_y is None or self.magnetic_field_z is None:
            return Result.failure(Error.validation("Magnetic field values are required"))

        if not (-1000 <= self.magnetic_field_x <= 1000):
            return Result.failure(Error.validation("Magnetic field X must be between -1000 and 1000"))

        if not (-1000 <= self.magnetic_field_y <= 1000):
            return Result.failure(Error.validation("Magnetic field Y must be between -1000 and 1000"))

        if not (-1000 <= self.magnetic_field_z <= 1000):
            return Result.failure(Error.validation("Magnetic field Z must be between -1000 and 1000"))

        return Result.success()

    def validate_location(self) -> Result[Success]:
        if self.latitude is None or self.longitude is None or self.altitude is None:
            return Result.failure(Error.validation("Location values are required"))

        if not (-90 <= self.latitude <= 90):
            return Result.failure(Error.validation("Latitude must be between -90 and 90"))

        if not (-180 <= self.longitude <= 180):
            return Result.failure(Error.validation("Longitude must be between -180 and 180"))

        if not (-500 <= self.altitude <= 9000):
            return Result.failure(Error.validation("Altitude must be between -500 and 9000"))

        return Result.success()
