"""Tests for openHAB api."""
import asyncio

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import pytest
from pytest_homeassistant_custom_component.common import load_fixture

from custom_components.openhab.api import ApiClientException, OpenHABApiClient


async def test_api(hass, aioclient_mock):
    """Test API calls."""

    # To test the api submodule, we first create an instance of our API client
    api = OpenHABApiClient(hass, "http://openhab:8080", "test", "test")

    # Use aioclient_mock which is provided by `pytest_homeassistant_custom_components`
    # to mock responses to aiohttp requests. In this case we are telling the mock to
    # return {"test": "test"} when a `GET` call is made to the specified URL. We then
    # call `async_get_items` which will make that `GET` request.
    aioclient_mock.get(
        "http://openhab:8080/rest/items", json=load_fixture("items.json")
    )
    assert await api.async_get_items()

    # We do the same for `async_set_title`. Note the difference in the mock call
    # between the previous step and this one. We use `patch` here instead of `get`
    # because we know that `async_set_title` calls `api_wrapper` with `patch` as the
    # first parameter
    aioclient_mock.get(
        "http://openhab:8080/rest/items/Wifi_Level", json=load_fixture("item.json")
    )
    assert await api.async_get_item("Wifi_Level") is None
