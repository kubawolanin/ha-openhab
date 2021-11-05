"""Constants for openHAB."""
from datetime import timedelta
from logging import Logger, getLogger

# Base component constants
NAME = "openHAB"
DOMAIN = "openhab"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by openHAB REST API"
ISSUE_URL = "https://github.com/kubawolanin/ha-openhab/issues"
DATA_COORDINATOR_UPDATE_INTERVAL = timedelta(seconds=15)
LOGGER: Logger = getLogger(__package__)

# Platforms
BINARY_SENSOR = "binary_sensor"
CAMERA = "camera"
COVER = "cover"
DEVICE_TRACKER = "device_tracker"
LIGHT = "light"
MEDIA_PLAYER = "media_player"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, COVER, DEVICE_TRACKER, LIGHT, SENSOR, SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_BASE_URL = "base_url"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN

ITEMS_MAP = {
    BINARY_SENSOR: ["Contact"],
    CAMERA: ["Image"],
    COVER: ["Rollershutter"],
    DEVICE_TRACKER: ["Location"],
    LIGHT: ["Color", "Dimmer"],
    MEDIA_PLAYER: ["Player"],
    SENSOR: [
        "DateTime",
        "Number",
        "Number:Length",
        "Number:Temperature",
        "Number:Pressure",
        "Number:Speed",
        "Number:Intensity",
        "Number:Dimensionless",
        "Number:Angle",
        "String",
    ],
    SWITCH: ["Switch"],
}

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
