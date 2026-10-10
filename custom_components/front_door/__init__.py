"""Front Door integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Front Door from a config entry."""

    return True


async def async_unload_entry(
        hass: HomeAssistant, 
        entry: ConfigEntry,
        ) -> bool:
        """Unload Front Door."""
        return True
