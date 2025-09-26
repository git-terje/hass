import logging
import aiohttp
from homeassistant.core import HomeAssistant, ServiceCall

DOMAIN = "ha_sysinfo"
_LOGGER = logging.getLogger(__name__)

API_LOGS = "/api/logs"
API_SUPERVISOR_LOGS = "/api/hassio/supervisor/logs"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up ha_sysinfo integration."""

    async def handle_get_logs(call: ServiceCall):
        lines = call.data.get("lines", 100)
        token = hass.data.get("auth_token")
        headers = {"Authorization": f"Bearer {token}"}

        async with aiohttp.ClientSession() as session:
            results = {}

            # Home Assistant logs
            try:
                async with session.get(f"{hass.config.api.base_url}{API_LOGS}", headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        filtered = [
                            f"[{log['level']}] {log['name']}: {log['message']}"
                            for log in data if log["level"] in ("ERROR", "WARNING")
                        ]
                        results["homeassistant"] = filtered[-lines:]
            except Exception as e:
                results["homeassistant"] = [f"Exception: {e}"]

            # Supervisor logs
            try:
                async with session.get(f"{hass.config.api.base_url}{API_SUPERVISOR_LOGS}", headers=headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        filtered = [line for line in text.splitlines() if "ERROR" in line or "WARNING" in line]
                        results["supervisor"] = filtered[-lines:]
            except Exception as e:
                results["supervisor"] = [f"Exception: {e}"]

        hass.bus.async_fire("ha_sysinfo_logs", results)
        _LOGGER.info("Filtered logs fetched (event: ha_sysinfo_logs)")

    hass.services.async_register(DOMAIN, "get_logs", handle_get_logs)
    return True
