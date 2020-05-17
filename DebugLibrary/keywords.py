import sys

from robot.libraries.BuiltIn import run_keyword_variant

from .debugcmd import DebugCmd
from .robotkeyword import run_debug_if
from .steplistener import RobotLibraryStepListenerMixin, is_step_mode
from .styles import print_output
from .webdriver import get_remote_url, get_session_id, get_webdriver_remote


class DebugKeywords(RobotLibraryStepListenerMixin):
    """Debug Keywords for RobotFramework."""

    def debug(self):
        """Open a interactive shell, run any RobotFramework keywords.

        Keywords separated by two space or one tab, and Ctrl-D to exit.
        """
        # re-wire stdout so that we can use the cmd module and have readline
        # support
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__

        show_intro = not is_step_mode()
        if show_intro:
            print_output('\n>>>>>', 'Enter interactive shell')

        self.debug_cmd = DebugCmd()
        if show_intro:
            self.debug_cmd.cmdloop()
        else:
            self.debug_cmd.cmdloop(intro='')

        show_intro = not is_step_mode()
        if show_intro:
            print_output('\n>>>>>', 'Exit shell.')

        # put stdout back where it was
        sys.stdout = old_stdout

    @run_keyword_variant(resolve=1)
    def debug_if(self, condition, *args):
        """Runs the Debug keyword if condition is true."""
        return run_debug_if(condition, *args)

    def get_remote_url(self):
        """Get selenium URL for connecting to remote WebDriver."""
        return get_remote_url()

    def get_session_id(self):
        """Get selenium browser session id."""
        return get_session_id()

    def get_webdriver_remote(self):
        """Print the way connecting to remote selenium server."""
        return get_webdriver_remote()
