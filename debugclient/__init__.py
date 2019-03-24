"""
DebugClient
Licensed under the MIT license (see `LICENSE` file)

Python client for interacting with DebugServer-js
"""
from debugclient.core import DebugServer, DebugSession
from debugclient.version import version_string as __version__

__author__ = "Cameron Webb (webbjcam@gmail.com)"

# Remove any imported modules we don't want exported
del core
del utils
del version
