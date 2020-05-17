# /local/bin/python
# -*- coding: utf-8 -*-
import os
import json

from org.bukkit.command import Command

__all__ = [
    'TextFormatting',
    'Config',
    'ConfigCommand'
]


class TextFormatting(object):

    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def player_message_formatter(self, *args):
        return u'§6[{}]§r '.format(self.plugin_name) + ' '.join(args)


class Config(object):
    """
    Configuration object.

    Attr:
        params (dict): Dictionary with key - parameter name (str),
            value - dictionary with 'value' (default value for parameter)
            and 'type' (type for this parameter)

    """
    __slots__ = ['logger', '_config_path', '_config_dir_path']
    available_params = []
    params_types = {}
    params = {}

    def __init__(self, params, logger, plugin_name, plugin_dir,
                 config_name='config.json'):
        """
        Make configuration object and parse (dump) config.json file.

        Attr:
            params (dict): Dictionary with key - parameter name (str),
                value - dictionary with 'value' (default value for parameter)
                and 'type' (type for this parameter)

        """
        for param, info in params.items():
            self.params[param] = info.get('value')
            self.params_types[param] = info.get('type')
            self.available_params.append(param)

        self.logger = logger
        self._config_dir_path = os.path.join(plugin_dir, plugin_name)
        self._config_path = os.path.join(self._config_dir_path, config_name)

        self.parse_config()

    def get_param(self, param):
        if param not in self.available_params:
            raise ValueError("Parameter '{}' not found".format(param))
        return self.params.get(param)

    def set_param(self, param, value):
        if param not in self.available_params:
            raise ValueError("Parameter '{}' not found".format(param))

        types = self.params_types.get(param)
        if not isinstance(value, types):
            raise ValueError("Value '{}' is not {}".format(value, str(types)))

        self.params[param] = value
        self.logger.info("Parameter {} value is changed to {}".format(
            param, value
        ))
        self.dump_config()

    def parse_config(self):
        # Create config directory and dump default values
        if not os.path.exists(self._config_path):
            self.dump_config()
            return False

        # Read config
        with open(self._config_path, 'r') as configuration:
            parsed_config = json.load(configuration, encoding='utf-8')

        if (not isinstance(parsed_config, dict)
            or parsed_config.keys() != self.available_params):
            raise ValueError(
                'Please provide {} params to {}'.format(
                    self.available_params, self._config_path
                )
            )

        for param, value in parsed_config.items():
            types = self.params_types.get(param)
            if not isinstance(value, types):
                raise ValueError(
                    'Please provide {} in {} type'.format(param, types)
                )
            self.params[param] = value

        self.logger.info('Loaded config: {}'.format(self.__dict__()))

        self.logger.info('§2Configuration has been parsed successfully!')
        return True

    def dump_config(self):
        if not os.path.exists(self._config_dir_path):
            os.mkdir(self._config_dir_path)

        with open(self._config_path, 'w') as config:
            json.dump(self.__dict__(), config)

        self.logger.info("For configurate plugin change: {}!".format(
            self._config_path
        ))
        self.logger.info("Configuration has been dumped to file!")

    def __dict__(self):
        return self.params

    def __str__(self):
        params_repr_list = [
            '{}={}'.format(key, value)
            for key, value in self.params.items()
        ]
        return ', '.join(params_repr_list)


# Command Handler
class ConfigCommand(Command):
    def __init__(self, name, config, player_formatter=None):
        Command.__init__(self, name)
        self.sub_commands = {
            'reload': self._reload,
            'params': self._params,
            'set': self._set
        }
        self.config = config
        if player_formatter is None:
            self._p = lambda *args: [' '] + args
        else:
            self._p = player_formatter

    def execute(self, caller, label, parameters):
        if not caller.isOp():
            caller.sendMessage(self._p("§4You don't have permission for this command!"))
            return True

        if not parameters or parameters[0] not in self.sub_commands.keys():
            caller.sendMessage(self._p('Available commands: {}'.format(', '.join(
                self.sub_commands
            ))))

        elif parameters[0] in self.sub_commands.keys():
            sub_command = parameters.pop(0)
            self.sub_commands[sub_command](caller, *parameters)

    def _reload(self, caller, *args):
        if args:
            caller.sendMessage(self._p('§4Arguments not provided!'))
            return

        result = self.config.parse_config()
        if result:
            caller.sendMessage(self._p('§2Configuration reloaded!'))
        elif result is None:
            caller.sendMessage(self._p('§4Error in loading config, check console!'))
        else:
            caller.sendMessage(self._p('§4Configuration file restored!'))

    def _params(self, caller, *args):
        if args:
            caller.sendMessage(self._p('§4Arguments not provided!'))
            return
        caller.sendMessage(self._p('Current params: {}'.format(str(self.config))))


    def _set(self, caller, *args):
        if not args or len(args) == 1:
            caller.sendMessage(self._p('Params available to set: {}'.format(
                ', '.join(self.config.available_params)
            )))
            return

        if len(args) > 2:
            caller.sendMessage(self._p('§4Invalid arguments count!'))
            return

        elif args[0] in self.config.available_params and len(args) == 2:
            key = args[0]
            try:
                type_ = self.config.params_types.get(key)
                value = type_(args[1])
            except ValueError as e:
                caller.sendMessage(self._p('§4Required {} value!'.format(
                    type(type_())
                )))
                return True

            try:
                self.config.set_param(key, value)
            except ValueError as e:
                caller.sendMessage(self._p('§4 {}!'.format(e)))
                return True
            caller.sendMessage(self._p('§2Param {} now is {}!'.format(key, value)))

        return True

    def tabComplete(self, sender, alias, args, location=None):
        if not sender.isOp():
            return []

        if not args[0]:
            return self.sub_commands.keys()

        elif len(args) == 1:
            return filter(lambda ch: ch.startswith(args[0]), self.sub_commands.keys())

        elif args[0] in self.sub_commands.keys():
            if args[0] == 'set':
                if len(args) == 2:
                    return self.config.available_params
                if args[1] in self.config.available_params and len(args) == 3:
                    return ['<int>']
            return []
