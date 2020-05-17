# random-respawn-pyplugin
[![GitHub](https://img.shields.io/github/license/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![GitHub All Releases](https://img.shields.io/github/downloads/dmytrohoi/random-respawn-pyplugin/total)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![Required](https://img.shields.io/badge/required-minecraft--python-blue)](https://github.com/Macuyiko/minecraft-python)
[![Spigot](https://img.shields.io/badge/spigot-1.15.2-orange)](https://www.spigotmc.org/)
## About

Minecraft Spigot plugin on [@minecraft-python](https://github.com/Macuyiko/minecraft-python) interpreter to make randomly player respawn.

This plugin provides a random spawn point for the player if he is killed.

## Installation

Install [@minecraft-python](https://github.com/Macuyiko/minecraft-python) first (_**required!**_).

[Download latest release](https://github.com/dmytrohoi/random-respawn-pyplugin/releases) and copy all files/directories to `/python-plugins/` server directory.

Run server.

## Configuration

You can configure the plugin using in-game (op permission is required!) or console command `/random-respawn set [x/z] <int>`, where:
 - `[x/z]` - chosen coordinate to calculate random player respawn coordinates from Minecraft spawn point;
 - `<int>` - max offset limits in chosen coordinate to calculate random player respawn coordinates from Minecraft spawn point.

Or replace values in `/python-plugins/random-respawn-pyplugin/config.json` file.

## FAQ

### Q: What are the default limits?

By default limits is `x=50`, `z=50`. Coordinate `y` is always on top of world.

### **Q**: Does not work with Essentials Spawn!

Please set the Essentials Spawn priority to `none`. In config.yml - `respawn-listener-priority: none`.

## Donation

If you like it, please use the Sponsor button at the top of this page on GitHub. 
Or [liberapay.com](https://liberapay.com/dmytrohoi) / [monobank.ua](https://dmytrohoi.com/donate).
