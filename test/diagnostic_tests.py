from src import *


# Test para validate_temperature
def test_validate_temperature_success():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), temperature=25
    )
    result = diagnostic.validate_temperature()
    assert result.is_success


def test_validate_temperature_failure():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), temperature=150
    )
    result = diagnostic.validate_temperature()
    assert result.is_failure
    assert result.first_error.message == "Temperature must be between -100 and 100"


# Test para validate_humidity
def test_validate_humidity_success():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), humidity=50
    )
    result = diagnostic.validate_humidity()
    assert result.is_success


def test_validate_humidity_failure():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), humidity=150
    )
    result = diagnostic.validate_humidity()
    assert result.is_failure
    assert result.first_error.message == "Humidity must be between 0 and 100"


# Test para validate_accelerations
def test_validate_accelerations_success():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        acceleration_x=10,
        acceleration_y=15,
        acceleration_z=5
    )
    result = diagnostic.validate_accelerations()
    assert result.is_success


def test_validate_accelerations_failure():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        acceleration_x=-200,
        acceleration_y=10,
        acceleration_z=5
    )
    result = diagnostic.validate_accelerations()
    assert result.is_failure
    assert result.first_error.message == "Acceleration X must be between -100 and 100"


# Test para validate_vibration
def test_validate_vibration_success():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), vibration=500
    )
    result = diagnostic.validate_vibration()
    assert result.is_success


def test_validate_vibration_failure():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), vibration=1500
    )
    result = diagnostic.validate_vibration()
    assert result.is_failure
    assert result.first_error.message == "Vibration must be between 0 and 1000"


# Test para validate_sound_level
def test_validate_sound_level_success():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), sound_level=100
    )
    result = diagnostic.validate_sound_level()
    assert result.is_success


def test_validate_sound_level_failure():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), sound_level=250
    )
    result = diagnostic.validate_sound_level()
    assert result.is_failure
    assert result.first_error.message == "Sound level must be between 0 and 200"


# Test para validate_battery_level
def test_validate_battery_level_success():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), battery_level=80
    )
    result = diagnostic.validate_battery_level()
    assert result.is_success


def test_validate_battery_level_failure():
    diagnostic = Diagnostic(
        id="sensor_1", device_id="device_1", timestamp=datetime.now(), battery_level=150
    )
    result = diagnostic.validate_battery_level()
    assert result.is_failure
    assert result.first_error.message == "Battery level must be between 0 and 100"


# Test para validate_magnetic_fields
def test_validate_magnetic_fields_success():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        magnetic_field_x=500,
        magnetic_field_y=-300,
        magnetic_field_z=200
    )
    result = diagnostic.validate_magnetic_fields()
    assert result.is_success


def test_validate_magnetic_fields_failure():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        magnetic_field_x=-1500,
        magnetic_field_y=100,
        magnetic_field_z=50
    )
    result = diagnostic.validate_magnetic_fields()
    assert result.is_failure
    assert result.first_error.message == "Magnetic field X must be between -1000 and 1000"


# Test para validate_location
def test_validate_location_success():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        latitude=45,
        longitude=-75,
        altitude=100
    )
    result = diagnostic.validate_location()
    assert result.is_success


def test_validate_location_failure():
    diagnostic = Diagnostic(
        id="sensor_1",
        device_id="device_1",
        timestamp=datetime.now(),
        latitude=-100,
        longitude=-75,
        altitude=100
    )
    result = diagnostic.validate_location()
    assert result.is_failure
    assert result.first_error.message == "Latitude must be between -90 and 90"
