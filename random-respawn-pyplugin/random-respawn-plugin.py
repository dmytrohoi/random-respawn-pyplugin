# /local/bin/python
# -*- coding: utf-8 -*-
# Plugin version: 0.0.1
import os
from random import randint

if os.name == 'java':
    from org.python.core import codecs
    codecs.setDefaultEncoding('utf-8')

from org.bukkit.event.player import PlayerRespawnEvent
from org.bukkit.plugin import EventExecutor
from org.bukkit.event import EventPriority

import mcapi
from pyplugin import utils, log, PLUGIN_NAME, PYPLUGINS_DIR_PATH


## Common
# Add event listener implementation
def add_event_listener(event_type, execfunc, priority=EventPriority.HIGH):
    listener = mcapi.EventListener(execfunc)
    executor = Executor()
    mcapi.SERVER.getPluginManager().registerEvent(
        event_type, listener, priority, executor, mcapi.PLUGIN
    )
    return listener


# EventExecutor implementation
class Executor(EventExecutor):
    def execute(self, listener, event):
        listener.execute(event)


# Event Handler
def respawn_randomly(event):
    """
    Handle PlayerRespawnEvent and provides respawning randomly around
    spawn point.

    """
    player = event.getPlayer()

    if event.isBedSpawn():
        player.sendMessage(_p('§2 Respawning in bed'))
        log.info(player.getDisplayName(), 'respawned in bed.')
        return True

    world_spawn_location = mcapi.WORLD.getSpawnLocation()

    # Add random values to respawn point
    x_limit = config.get_param('x')
    z_limit = config.get_param('z')

    x_position = randint(-x_limit, x_limit)
    z_position = randint(-z_limit, z_limit)

    random_respawn_location = world_spawn_location.add(x_position, 0, z_position)

    # Choose block coordinates for spawn in height of the ground
    block_y = random_respawn_location.getBlockY()
    random_respawn_location.setY(block_y + 1)

    event.setRespawnLocation(random_respawn_location)
    player.sendMessage(_p('You are respawned in random location around spawn!'))
    log.info(player.getDisplayName(), 'respawned in random location.')


## Start building plugin
plugin_parameters = {
    'x': {'value': 50, 'type': int},
    'z': {'value': 50, 'type': int},
}

# Create helpers
message_formater = utils.TextFormatting('Random Spawn')
_p = message_formater.player_message_formatter
config = utils.Config(plugin_parameters, log, PLUGIN_NAME, PYPLUGINS_DIR_PATH)

# Register listeners and command
add_event_listener(PlayerRespawnEvent, respawn_randomly)
config_command = utils.ConfigCommand("random-respawn", config, _p)
mcapi._commandMap.register("random-respawn", config_command)
