# random-respawn-pyplugin
[![GitHub](https://img.shields.io/github/license/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/dmytrohoi/random-respawn-pyplugin)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![GitHub All Releases](https://img.shields.io/github/downloads/dmytrohoi/random-respawn-pyplugin/total)](https://github.com/dmytrohoi/random-respawn-pyplugin/releases)
[![Required](https://img.shields.io/badge/required-PyPlugins-blue)](https://github.com/pyplugins/pyplugins)
[![Spigot](https://img.shields.io/badge/spigot-1.15.2-orange)](https://www.spigotmc.org/resources/random-respawn.78929/)
[![Spiget Downloads](https://img.shields.io/spiget/downloads/78929)](https://www.spigotmc.org/resources/random-respawn.78929/)
[![Spiget Stars](https://img.shields.io/spiget/rating/78929)](https://www.spigotmc.org/resources/random-respawn.78929/)
[![Spiget tested server versions](https://img.shields.io/spiget/tested-versions/78929)](https://www.spigotmc.org/resources/random-respawn.78929/)
[![bStats Players](https://img.shields.io/bstats/players/7640)](https://www.spigotmc.org/resources/random-respawn.78929/)
[![bStats Servers](https://img.shields.io/bstats/servers/7640)](https://www.spigotmc.org/resources/random-respawn.78929/)



## About

Minecraft Spigot plugin on [@pyplugins](https://github.com/pyplugins/pyplugins) interpreter to make randomly player respawn.

This plugin provides a random spawn point for the player if he is killed.

## Installation

Install [@pyplugins](https://github.com/pyplugins/pyplugins) first (_**required!**_).

[Download latest release](https://github.com/dmytrohoi/random-respawn-pyplugin/releases) and copy file to `server/plugins/` directory.

Run server.

## Configuration

You can configure the plugin using in-game (operator permission is required!) or console command `/random-respawn-config set [x/z] <int>`, where:
 - `[x/z]` - chosen coordinate to calculate random player respawn coordinates from Minecraft spawn point;
 - `<int>` - max offset limits in chosen coordinate to calculate random player respawn coordinates from Minecraft spawn point.

Or replace values in `/plugins/RandomRespawn/config.yml` file.

## FAQ

### Q: What are the default limits?

By default limits are `x=50`, `z=50`. Coordinate `y` is always on top of world.

### **Q**: Does not work with Essentials Spawn!

Please set the Essentials Spawn priority to `none`. In config.yml - `respawn-listener-priority: none`.

## Donation

If you like it, please use the Sponsor button at the top of this page on GitHub.
Or [liberapay.com](https://liberapay.com/dmytrohoi) / [monobank.ua](https://dmytrohoi.com/donate).
