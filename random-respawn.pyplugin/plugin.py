
# /local/bin/python
# -*- coding: utf-8 -*-
"""
File: plugin.py
Version: 0.0.2
Author: hedgehoi (Dmytro Hoi)
License: MIT License

Dependencies:
    - PyPlugins v0.0.1 / https://github.com/pyplugins/pyplugins

"""
from random import randint

from org.bukkit.event.player import PlayerRespawnEvent


class RespawnListener(PythonListener):
    listeners = [
        PyEventHandler('onPlayerRespawn', PlayerRespawnEvent)
    ]

    def onPlayerRespawn(self, event):
        """
        Handle PlayerRespawnEvent and provides respawning randomly around
        spawn point.

        """
        player = event.getPlayer()
        plugin_name = self.plugin.getName()
        plugin_prefix = u'[\u00a74{}\u00a7r]'.format(plugin_name)
        if event.isBedSpawn():
            player.sendMessage(plugin_prefix + u'\u00a72 Respawning in bed')
            self.plugin.logger.info(player.getDisplayName() + ' respawned in bed.')
            return True

        world = Bukkit.getServer().getWorlds().get(0)
        world_spawn_location = world.getSpawnLocation()

        # Add random values to respawn point
        x_limit = self.plugin.config.getInt('x')
        z_limit = self.plugin.config.getInt('z')

        x_position = randint(-x_limit, x_limit)
        z_position = randint(-z_limit, z_limit)

        random_respawn_location = world_spawn_location.add(x_position, 0, z_position)

        # Choose block coordinates for spawn in height of the ground
        block_y = random_respawn_location.getBlockY()
        random_respawn_location.setY(block_y + 1)

        event.setRespawnLocation(random_respawn_location)
        player.sendMessage(plugin_prefix + ' You are respawned in random location around spawn!')
        self.plugin.logger.info(player.getDisplayName() + ' respawned in random location.')


class RandomRespawnPlugin(PythonPlugin):

    def onEnable(self):

        pm = self.getServer().getPluginManager()
        pm.registerEvents(RespawnListener(self), self)
        # Add configuration
        self.add_configuration(available_options=[
            ('x', int), ('z', int)
        ])
        # Add bStats metrics
        self.add_bstats(7640)
        self.logger.info("plugin enabled!")

    def onDisable(self):
        self.logger.info("plugin disabled!")
