"""Config flow for Front Door integration"""

from homeassistant import config_entries
from homeassistant.core import HomeAssistant


class FrontDoorConfigFlow(config_entries.ConfigFlow, domain="front_door"):
    """Handle a config flow for Front Door integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Front Door",
                data=user_input
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            
        )