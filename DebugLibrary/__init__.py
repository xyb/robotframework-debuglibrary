from .keywords import DebugKeywords
from .version import VERSION

"""A debug library and REPL for RobotFramework."""


class DebugLibrary(DebugKeywords):
    """Debug Library for RobotFramework."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION
