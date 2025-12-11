"""Light platform for Wordclock."""
from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
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
    """Set up the Wordclock light."""
    coordinator: WordclockCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WordclockLight(coordinator)])


class WordclockLight(CoordinatorEntity, LightEntity):
    """Representation of the Wordclock Light."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB

    def __init__(self, coordinator: WordclockCoordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.base_url}_light"

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        # If brightness is > 0, we consider it on.
        return self.coordinator.data["brightness"] > 0

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        return self.coordinator.data["brightness"]

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return the rgb color value [int, int, int]."""
        # We use the 'words' color as the main color for the light entity
        # or 'all' if they are synced. The API returns 'words', 'minutes', 'background'.
        # Let's use 'words' as the primary color.
        words_color = self.coordinator.data["colors"].get("words", {})
        return (
            words_color.get("red", 255),
            words_color.get("green", 255),
            words_color.get("blue", 255),
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        if ATTR_RGB_COLOR in kwargs:
            r, g, b = kwargs[ATTR_RGB_COLOR]
            await self.coordinator.set_color(r, g, b, color_type="all")

        if ATTR_BRIGHTNESS in kwargs:
            await self.coordinator.set_brightness(kwargs[ATTR_BRIGHTNESS])
        elif not self.is_on:
            # If turning on without brightness specified, set to max or restore?
            # The API doesn't seem to have a "turn on" without brightness.
            # If we are "off" (brightness 0), we should set it to something visible.
            # Let's default to 255 if it was 0.
            await self.coordinator.set_brightness(255)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self.coordinator.set_brightness(0)
