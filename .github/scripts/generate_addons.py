import json
import os

addons = {}
for addon_dir in os.listdir("addons"):
    cfg = os.path.join("addons", addon_dir, "config.json")
    if os.path.exists(cfg):
        with open(cfg) as f:
            conf = json.load(f)
            addons[addon_dir] = {
                "name": conf["name"],
                "version": conf["version"],
                "slug": conf["slug"],
                "description": conf.get("description", ""),
                "arch": conf.get("arch", []),
                "url": conf.get("url", ""),
            }

with open("addons.json", "w") as f:
    json.dump(addons, f, indent=2)
