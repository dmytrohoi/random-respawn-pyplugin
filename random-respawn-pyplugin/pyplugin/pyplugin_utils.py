# /local/bin/python
# -*- coding: utf-8 -*-
import os
import json
import yaml

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
        params (dict): Dictionary with:
                key - parameter name (str),
                value - dictionary with:
                'value' - default value for parameter,
                'type' - type for this parameter,
                'hide' - (optional) prevent changing by in-game/console
                    'set' command,
                'description' - (optional) information about the parameter
                    for add to the header in a config file.

    """
    __slots__ = ['logger', '_config_path', '_config_dir_path', 'plugin_name']
    available_params = []
    hide_params = []
    params_types = {}
    params = {}
    params_descriptions = {}

    def __init__(self, params, logger, plugin_name, plugin_dir,
                 config_name='config.yml'):
        """
        Make configuration object and parse (dump) config file.

        Attr:
            params (dict): Dictionary with:
                  key - parameter name (str),
                  value - dictionary with:
                    'value' - default value for parameter,
                    'type' - type for this parameter,
                    'hide' - (optional) prevent changing by in-game/console
                        'set' command,
                    'description' - (optional) information about the parameter
                        for add to the header in a config file.

        Example:
        {
            'x': {
                'value': 50, 'type': int,
                'description': 'max random limit (mean -x..x) in x coordinate,'
                            'must be an integer value (default: 50)',
            },
            'z': {
                'value': 50, 'type': int,
                'description': 'max random limit (mean -z..z) in z coordinate,'
                            'must be an integer value (default: 50)',
            },
        }

        """
        for param, info in params.items():
            self.params[param] = info.get('value')
            self.params_types[param] = info.get('type')
            self.available_params.append(param)
            if info.get('hide'):
                self.hide_params.append(param)
            if info.get('description'):
                self.params_descriptions[param] = info.get('description')

        self.logger = logger
        self.plugin_name = plugin_name
        self._config_dir_path = os.path.join(plugin_dir, self.plugin_name)
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
            parsed_config = yaml.safe_load(configuration)

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
        # Construct config header
        header = self._construct_config_header()

        if not os.path.exists(self._config_dir_path):
            os.mkdir(self._config_dir_path)
        with open(self._config_path, 'w') as config:
            # Add header
            config.write(header)
            # Dump parameters
            yaml.safe_dump(self.__dict__(), config)

        self.logger.info("For configurate plugin change: {}!".format(
            self._config_path
        ))
        self.logger.info("Configuration has been dumped to file!")

    def _construct_config_header(self):
        header = '# {} configuration file\n'.format(self.plugin_name)

        if not self.params_descriptions:
            return header

        params_descriptions = [
            '{}: {}'.format(key, desc)
            for key, desc in self.params_descriptions.items()
        ]
        descriptions = '# Parameters:\n#\t{}\n\n'.format(
            '\n#\t'.join(params_descriptions)
        )
        return header + descriptions

    def __dict__(self):
        return self.params

    def __str__(self):
        params_repr_list = [
            '{}={}'.format(key, value)
            for key, value in self.params.items()
            if key not in self.hide_params
        ]
        return ', '.join(params_repr_list)


# Command Handler
class ConfigCommand(Command):
    def __init__(self, name, config, player_formatter=None):
        Command.__init__(self, name)
        self.sub_commands = {
            'reload': self._reload_subcommand,
            'params': self._params_subcommand,
            'set': self._set_subcommand
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
            self.sub_commands[sub_command](caller, parameters)

    def _reload_subcommand(self, caller, args):
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

    def _params_subcommand(self, caller, args):
        if args:
            caller.sendMessage(self._p('§4Arguments not provided!'))
            return
        caller.sendMessage(self._p('Current params: {}'.format(str(self.config))))


    def _set_subcommand(self, caller, args):
        params = filter(lambda key: key not in self.config.hide_params,
                        self.config.available_params)

        arguments_length = len(args)

        if arguments_length > 2:
            caller.sendMessage(self._p('§4Invalid arguments count!'))

        elif arguments_length == 2 and args[0] in params:
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
            return

        caller.sendMessage(self._p('Params available to set: {}'.format(
            ', '.join(params)
        )))
        return True

    def tabComplete(self, sender, alias, args, location=None):
        if not sender.isOp():
            return []

        sub_command = args[0]
        args_count = len(args)
        if not sub_command:
            return self.sub_commands.keys()

        elif args_count == 1:
            return filter(lambda ch: ch.startswith(args[0]),
                          self.sub_commands.keys())

        elif sub_command in self.sub_commands.keys():
            if sub_command != 'set':
                return []

            # Filter available params to set by command
            params = filter(lambda key: key not in self.config.hide_params,
                            self.config.available_params)
            param_arg = args[1]

            if args_count == 2 and not param_arg:
                return params
            elif args_count == 2:
                return filter(lambda ch: ch.startswith(param_arg), params)
            elif args_count == 3 and param_arg in params and not param_arg:
                return ['{}'.format(self.config.params_types[param_arg])]
