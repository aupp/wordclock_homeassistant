"""The Wordclock integration."""
from __future__ import annotations

import logging
import async_timeout
from datetime import timedelta

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.LIGHT, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wordclock from a config entry."""
    
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    base_url = f"http://{host}:{port}/api"
    session = async_get_clientsession(hass)

    coordinator = WordclockCoordinator(hass, session, base_url)
    
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(hass, entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(hass, entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class WordclockCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Wordclock data."""

    def __init__(self, hass, session, base_url):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )
        self.session = session
        self.base_url = base_url

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                # Fetch all needed data
                # 1. Current Plugin
                async with self.session.get(f"{self.base_url}/plugin") as resp:
                    resp.raise_for_status()
                    current_plugin_data = await resp.json()
                    current_plugin = current_plugin_data.get("plugin", {})

                # 2. All Plugins (we might only need this once, but good to have if they change)
                async with self.session.get(f"{self.base_url}/plugins") as resp:
                    resp.raise_for_status()
                    all_plugins_data = await resp.json()
                    all_plugins = all_plugins_data.get("plugins", [])

                # 3. Colors
                async with self.session.get(f"{self.base_url}/color") as resp:
                    resp.raise_for_status()
                    colors = await resp.json()

                # 4. Brightness
                async with self.session.get(f"{self.base_url}/brightness") as resp:
                    resp.raise_for_status()
                    brightness = await resp.json()

                return {
                    "current_plugin": current_plugin,
                    "all_plugins": all_plugins,
                    "colors": colors,
                    "brightness": brightness
                }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def set_plugin(self, plugin_name):
        """Set the active plugin."""
        async with self.session.post(f"{self.base_url}/plugin", json={"name": plugin_name}) as resp:
            resp.raise_for_status()
        await self.async_request_refresh()

    async def set_color(self, red, green, blue, color_type="all"):
        """Set the color."""
        payload = {"red": red, "green": green, "blue": blue, "type": color_type}
        async with self.session.post(f"{self.base_url}/color", json=payload) as resp:
            resp.raise_for_status()
        await self.async_request_refresh()

    async def set_brightness(self, brightness):
        """Set the brightness."""
        async with self.session.post(f"{self.base_url}/brightness", json={"brightness": brightness}) as resp:
            resp.raise_for_status()
        await self.async_request_refresh()
