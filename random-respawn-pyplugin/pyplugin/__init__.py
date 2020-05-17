# /local/bin/python
# -*- coding: utf-8 -*-
"""
PyPlugin Helpers
"""
import os
import inspect

import pyplugin_utils as utils
from pyplugin_logging import Logger


__all__ = [
    'utils',
    'log'
    'PLUGIN_NAME',
    'PYPLUGINS_DIR_PATH',
]
__version__ = '0.0.1'


if __name__ != '__main__':
    # Get info where pyplugin framework is imported
    imported_from = inspect.stack()[1][1]
    # Get plugin folder path and name
    PYPLUGINS_DIR_PATH = os.path.dirname(imported_from)
    PLUGIN_NAME = os.path.splitext(os.path.basename(imported_from))[0]
    # Make default logger
    log = Logger(PLUGIN_NAME)
