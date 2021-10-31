# openHAB custom integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [openhab][openhab]._

**This component will set up the following platforms.**

| Platform        | Description                         |
| --------------- | ----------------------------------- |
| `binary_sensor` | Show something `True` or `False`.   |
| `sensor`        | Show info from blueprint API.       |
| `switch`        | Switch something `True` or `False`. |

![example][exampleimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `openhab`.
4. Download _all_ the files from the `custom_components/openhab/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "openHAB"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/openhab/translations/en.json
custom_components/openhab/translations/nb.json
custom_components/openhab/translations/sensor.nb.json
custom_components/openhab/__init__.py
custom_components/openhab/api.py
custom_components/openhab/binary_sensor.py
custom_components/openhab/config_flow.py
custom_components/openhab/const.py
custom_components/openhab/manifest.json
custom_components/openhab/sensor.py
custom_components/openhab/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[openhab]: https://github.com/kubawolanin/ha-openhab
[buymecoffee]: https://www.buymeacoffee.com/kubawolanin
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/kubawolanin/blueprint.svg?style=for-the-badge
[commits]: https://github.com/kubawolanin/ha-openhab/commits/master
[hacs]: https://github.com/ludeeus/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/kubawolanin/ha-openhabblueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40kubawolanin-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kubawolanin/ha-openhab.svg?style=for-the-badge
[releases]: https://github.com/kubawolanin/ha-openhab/releases
