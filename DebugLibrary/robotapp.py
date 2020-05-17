
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.running.signalhandler import STOP_SIGNAL_MONITOR


def get_robot_instance():
    """Get robotframework builtin instance as context."""
    return BuiltIn()


def reset_robotframework_exception():
    """Resume RF after press ctrl+c during keyword running."""
    if STOP_SIGNAL_MONITOR._signal_count:
        STOP_SIGNAL_MONITOR._signal_count = 0
        STOP_SIGNAL_MONITOR._running_keyword = True
        logger.info('Reset last exception of DebugLibrary')
