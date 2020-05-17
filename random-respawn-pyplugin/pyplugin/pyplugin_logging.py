# /local/bin/python
# -*- coding: utf-8 -*-
__all__ = [
    'Logger',
]


class Logger(object):
    """
    Logging plugin information to console.

    Methods:
        log - provides sending simple message to console;
        info - sending message with tag INFO;
        error - sending message with tag ERROR;
        warning - sending message with tag WARNING;

    NOTE: Methods catches all string convertible value positional arguments
        (NOT dict, tuple or list).

    Attrs:
        plugin_name (str): name of the plugin that will be written in
            the console.

    """
    def __init__(self, plugin_name):
        """
        Initiate logger object to provide methods usage.

        Attrs:
            plugin_name (str): name of the plugin that will be written in
                the console.

        """
        self.plugin_name = plugin_name

    def log(self, *args):
        """Simple send message to console."""
        print('[§6{}§r] '.format(self.plugin_name) + ' '.join(args))

    def info(self, *args):
        """Send info message to console."""
        info_format = '[§bINFO§r]'
        self.log(info_format, *args)

    def error(self, *args):
        """Send error message to console."""
        error_format = '[§4ERROR§r]'
        self.log(error_format, *args)

    def warning(self, *args):
        """Send warning message to console."""
        warning_format = '[§eWARNING§r]'
        self.log(warning_format, *args)
