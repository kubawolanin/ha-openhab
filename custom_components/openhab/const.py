"""Constants for openhab."""
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

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_BASE_URL = "base_url"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN

ITEMS_MAP = {
    "Color": "light",
    "Dimmer": "light",
    "Contact": "binary_sensor",
    "DateTime": "sensor",
    "Number": "sensor",
    "String": "sensor",
    "Switch": "switch",
    # "Group": "",
    "Image": "camera",
    "Location": "zone",
    "Player": "media_player",
    "Rollershutter": "cover",
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
