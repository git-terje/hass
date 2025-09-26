from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "ha_sysinfo"

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """YAML-basert oppsett (fallback)."""
    if DOMAIN in config:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": "import"}
            )
        )
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Sett opp fra UI (config flow)."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Kalles når integrasjonen fjernes via UI."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
