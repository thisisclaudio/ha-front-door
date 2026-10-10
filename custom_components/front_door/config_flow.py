"""Config flow for Front Door integration"""

from __future__ import annotations

import voluptuous as vol
from serial.tools import list_ports

from .const import CONF_SERIAL_DEVICE, DOMAIN


from homeassistant import config_entries
from homeassistant.core import HomeAssistant


def _get_serial_ports():
    """Get a list of available serial ports."""
    return list(list_ports.comports())

def _port_label(port) -> str:
    """Return a label for a serial port."""
    description = port.description or "Unknown USB serial device"

    details = []

    if port.manufacturer:
        details.append(port.manufacturer)
    if port.product and port.product != description:
        details.append(port.product)

    if details:
        return f"{description} ({','.join(details)}) - {port.device}"

    return f"{description} - {port.device}"


class FrontDoorConfigFlow(config_entries.ConfigFlow, domain="front_door"):
    """Handle a config flow for Front Door integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        ports = await self.hass.async_add_executor_job(_get_serial_ports)

        if not ports:
            return self.async_abort(reason="no_serial_ports")

        
        if user_input is not None:
            selected_device = user_input[CONF_SERIAL_DEVICE]

            selected_port = next(
                (
                    port 
                    for port in ports 
                    if port.device == selected_device
                ),
                None,
            )

            if selected_port is None:
                return self.async_step_user()
            

            return self.async_create_entry(
                title=_port_label(selected_port),
                data={
                    CONF_SERIAL_DEVICE: selected_port.device,
                    "vid": selected_port.vid,
                    "pid": selected_port.pid,
                    "serial_number": selected_port.serial_number,
                    "manufacturer": selected_port.manufacturer,
                    "product": selected_port.product,
                },
            )

        port_options = {
            port.device: _port_label(port)
            for port in ports
        }

        schema = vol.Schema(
            {
            vol.Required(CONF_SERIAL_DEVICE): vol.In(port_options)
            }
        )

        # Show the form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            
        )