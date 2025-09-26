from homeassistant import config_entries
from homeassistant.core import callback
from . import DOMAIN

class HASysinfoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HA Sysinfo."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Håndter oppsett via UI."""
        if user_input is not None:
            return self.async_create_entry(title="HA Sysinfo", data={})

        return self.async_show_form(step_id="user", data_schema=None)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HASysinfoOptionsFlow(config_entry)

class HASysinfoOptionsFlow(config_entries.OptionsFlow):
    """Opsjoner (ikke brukt nå)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=None)
