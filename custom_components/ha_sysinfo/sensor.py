import logging
import aiohttp
from datetime import timedelta
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=1)

API_INFO = "/api/info"
API_HASSIO_INFO = "/api/hassio/info"
API_ADDONS = "/api/hassio/addons"
API_INTEGRATIONS = "/api/config/config_entries"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Sett opp ha_sysinfo sensorer."""
    token = hass.data.get("auth_token")  # må settes via config/secrets.yaml
    url = hass.config.api.base_url
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async_add_entities([
        HASensor(hass, url + API_INFO, headers, "HA Version", "version"),
        HASensor(hass, url + API_HASSIO_INFO, headers, "OS", "os_name"),
        HASensor(hass, url + API_HASSIO_INFO, headers, "CPU Arch", "arch"),
        HASensor(hass, url + API_HASSIO_INFO, headers, "Python", "python_version"),
        HASensor(hass, url + API_HASSIO_INFO, headers, "Supervisor", "supervisor"),
        HASensor(hass, url + API_HASSIO_INFO, headers, "Disk Used", ["host", "disk_used"]),
        HASensor(hass, url + API_HASSIO_INFO, headers, "Memory Used", ["host", "memory_used"]),
        AddonsSensor(hass, url + API_ADDONS, headers, "Installed Addons"),
        IntegrationsSensor(hass, url + API_INTEGRATIONS, headers, "Installed Integrations"),
        LogSummarySensor(hass, token, "HA Sysinfo Log Summary")
    ], True)


class HASensor(Entity):
    """Generisk sensor for systeminfo."""

    def __init__(self, hass, url, headers, name, key):
        self.hass = hass
        self.url = url
        self.headers = headers
        self._attr_name = name
        self.key = key
        self._state = None

    @property
    def state(self):
        return self._state

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    result = data.get("data", data)
                    if isinstance(self.key, list):
                        for k in self.key:
                            result = result.get(k, {})
                        self._state = result if result else "unknown"
                    else:
                        self._state = result.get(self.key, "unknown")
                else:
                    self._state = f"Error {resp.status}"


class AddonsSensor(Entity):
    """Sensor som viser installerte add-ons."""

    def __init__(self, hass, url, headers, name):
        self.hass = hass
        self.url = url
        self.headers = headers
        self._attr_name = name
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return len(self._attr_extra_state_attributes)

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    addons = data.get("data", {}).get("addons", [])
                    addons_info = {}
                    for addon in addons:
                        addons_info[addon["name"]] = {
                            "version": addon.get("version"),
                            "state": addon.get("state"),
                            "hostname": addon.get("hostname"),
                            "ingress": addon.get("ingress_url"),
                            "ports": addon.get("network", {})
                        }
                    self._attr_extra_state_attributes = addons_info
                else:
                    self._state = f"Error {resp.status}"


class IntegrationsSensor(Entity):
    """Sensor som viser installerte integrasjoner."""

    def __init__(self, hass, url, headers, name):
        self.hass = hass
        self.url = url
        self.headers = headers
        self._attr_name = name
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return len(self._attr_extra_state_attributes)

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    integrations = {}
                    for entry in data:
                        integrations[entry["title"]] = {
                            "domain": entry["domain"],
                            "state": entry["state"],
                            "source": entry["source"]
                        }
                    self._attr_extra_state_attributes = integrations
                else:
                    self._state = f"Error {resp.status}"


class LogSummarySensor(Entity):
    """Sensor som viser status for logger (OK/Feil oppdaget)."""

    def __init__(self, hass, token, name="HA Sysinfo Log Summary"):
        self.hass = hass
        self.token = token
        self._attr_name = name
        self._state = "unknown"
        self._attr_extra_state_attributes = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    async def async_update(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        base_url = self.hass.config.api.base_url
        ha_errors, sup_errors = [], []

        async with aiohttp.ClientSession() as session:
            # Home Assistant logs
            try:
                async with session.get(f"{base_url}/api/logs", headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        ha_errors = [
                            f"[{log['level']}] {log['name']}: {log['message']}"
                            for log in data if log["level"] in ("ERROR", "WARNING")
                        ]
            except Exception as e:
                ha_errors.append(f"Exception: {e}")

            # Supervisor logs
            try:
                async with session.get(f"{base_url}/api/hassio/supervisor/logs", headers=headers) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        sup_errors = [line for line in text.splitlines() if "ERROR" in line or "WARNING" in line]
            except Exception as e:
                sup_errors.append(f"Exception: {e}")

        if ha_errors or sup_errors:
            self._state = "Feil oppdaget"
        else:
            self._state = "OK"

        self._attr_extra_state_attributes = {
            "homeassistant": ha_errors[-5:],
            "supervisor": sup_errors[-5:]
      }
