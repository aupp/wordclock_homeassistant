"""Switch platform for Wordclock."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from . import WordclockCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Wordclock switches."""
    coordinator: WordclockCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create a switch for each available plugin
    plugins = coordinator.data.get("all_plugins", [])
    entities = []
    for plugin in plugins:
        entities.append(WordclockPluginSwitch(coordinator, plugin))
    
    async_add_entities(entities)


class WordclockPluginSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Wordclock Plugin Switch."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WordclockCoordinator, plugin_data: dict) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._plugin_name = plugin_data["name"]
        self._pretty_name = plugin_data.get("pretty_name", self._plugin_name)
        self._attr_name = self._pretty_name
        self._attr_unique_id = f"{coordinator.base_url}_plugin_{self._plugin_name}"
        self._attr_icon = "mdi:puzzle" # Default icon, maybe customize based on plugin name?

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        current_plugin = self.coordinator.data.get("current_plugin", {})
        return current_plugin.get("name") == self._plugin_name

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.set_plugin(self._plugin_name)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # If we turn off the active plugin, what should happen?
        # Ideally, we shouldn't be able to turn off the active plugin without selecting another.
        # But for a switch entity, we can just do nothing or maybe switch to a default.
        # Let's do nothing for now, as turning off a "mode" is ambiguous.
        # Or maybe we can log a warning.
        pass
