"""Constants for openHAB tests."""
from custom_components.openhab.const import CONF_BASE_URL, CONF_PASSWORD, CONF_USERNAME

# Mock config data to be used across multiple tests
MOCK_CONFIG = {
    CONF_BASE_URL: "http://openhab:8080",
    CONF_USERNAME: "test_username",
    CONF_PASSWORD: "test_password",
}
