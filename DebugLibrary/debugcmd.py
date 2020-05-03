import os

from robot.api import logger
from robot.errors import ExecutionFailed, HandlerExecutionFailed

from .cmdcompleter import CmdCompleter
from .prompttoolkitcmd import PromptToolkitCmd
from .robotapp import get_robot_instance, reset_robotframework_exception
from .robotkeyword import get_keywords, get_lib_keywords, run_keyword
from .robotlib import get_builtin_libs, get_libs, get_libs_dict, match_libs
from .robotselenium import SELENIUM_WEBDRIVERS, start_selenium_commands
from .robotvar import assign_variable
from .styles import (DEBUG_PROMPT_STYLE, get_debug_prompt_tokens, print_error,
                     print_output)

HISTORY_PATH = os.environ.get('RFDEBUG_HISTORY', '~/.rfdebug_history')


def run_robot_command(robot_instance, command):
    """Run command in robotframewrk environment."""
    if not command:
        return

    result = ''
    try:
        result = run_keyword(robot_instance, command)
    except ExecutionFailed as exc:
        print_error('! keyword:', command)
        print_error('! execution failed:', str(exc))
    except HandlerExecutionFailed as exc:
        print_error('! keyword:', command)
        print_error('! handler execution failed:', exc.full_message)
    except Exception as exc:
        print_error('! keyword:', command)
        print_error('! FAILED:', repr(exc))

    if result:
        head, message = result
        print_output(head, message)


class DebugCmd(PromptToolkitCmd):
    """Interactive debug shell for robotframework."""

    prompt_style = DEBUG_PROMPT_STYLE

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        PromptToolkitCmd.__init__(self, completekey, stdin, stdout,
                                  history_path=HISTORY_PATH)
        self.robot = get_robot_instance()

    def get_prompt_tokens(self, prompt_text):
        return get_debug_prompt_tokens(prompt_text)

    def postcmd(self, stop, line):
        """Run after a command."""
        return stop

    def pre_loop(self):
        """Reset robotframework before every loop iteration."""
        reset_robotframework_exception()

    def do_help(self, arg):
        """Show help message."""
        if not arg.strip():
            print('''\
Input Robotframework keywords, or commands listed below.
Use "libs" or "l" to see available libraries,
use "keywords" or "k" see the list of library keywords,
use the TAB keyboard key to autocomplete keywords.
Access https://github.com/xyb/robotframework-debuglibrary for more details.\
''')

        PromptToolkitCmd.do_help(self, arg)

    def get_completer(self):
        """Get completer instance specified for robotframework."""
        # commands
        commands = [(cmd_name, cmd_name, 'DEBUG command: {0}'.format(doc))
                    for cmd_name, doc in self.get_helps()]

        # libraries
        for lib in get_libs():
            commands.append((
                lib.name,
                lib.name,
                'Library: {0} {1}'.format(lib.name, lib.version),
            ))

        # keywords
        for keyword in get_keywords():
            # name with library
            name = '{0}.{1}'.format(keyword['lib'], keyword['name'])
            commands.append((
                name,
                keyword['name'],
                'Keyword: {0}'.format(keyword['doc']),
            ))
            # name without library
            commands.append((
                keyword['name'],
                keyword['name'],
                'Keyword[{0}.]: {1}'.format(keyword['lib'], keyword['doc']),
            ))

        return CmdCompleter(commands, self)

    def do_selenium(self, arg):
        """Start a selenium webdriver and open url in browser you expect.

        s(elenium)  [<url>]  [<browser>]

        default url is google.com, default browser is firefox.
        """

        for command in start_selenium_commands(arg):
            print_output('#', command)
            run_robot_command(self.robot, command)

    do_s = do_selenium

    def complete_selenium(self, text, line, begin_idx, end_idx):
        """Complete selenium command."""
        if len(line.split()) == 3:
            command, url, driver_name = line.lower().split()
            return [driver for driver in SELENIUM_WEBDRIVERS
                    if driver.startswith(driver_name)]
        elif len(line.split()) == 2 and line.endswith(' '):
            return SELENIUM_WEBDRIVERS
        return []

    complete_s = complete_selenium

    def default(self, line):
        """Run RobotFramework keywords."""
        command = line.strip()

        run_robot_command(self.robot, command)

    def do_libs(self, args):
        """Print imported and builtin libraries, with source if `-s` specified.

        l(ibs) [-s]
        """
        print_output('<', 'Imported libraries:')
        for lib in get_libs():
            print_output('   {}'.format(lib.name), lib.version)
            if lib.doc:
                logger.console('       {}'.format(lib.doc.split('\n')[0]))
            if '-s' in args:
                logger.console('       {}'.format(lib.source))
        print_output('<', 'Builtin libraries:')
        for name in sorted(get_builtin_libs()):
            print_output('   ' + name, '')

    do_l = do_libs

    def complete_libs(self, text, line, begin_idx, end_idx):
        """Complete libs command."""
        if len(line.split()) == 1 and line.endswith(' '):
            return ['-s']
        return []

    complete_l = complete_libs

    def do_keywords(self, args):
        """Print keywords of libraries, all or starts with <lib_name>.

        k(eywords) [<lib_name>]
        """
        lib_name = args
        matched = match_libs(lib_name)
        if not matched:
            print_error('< not found library', lib_name)
            return
        libs = get_libs_dict()
        for name in matched:
            lib = libs[name]
            print_output('< Keywords of library', name)
            for keyword in get_lib_keywords(lib):
                print_output('   {}\t'.format(keyword['name']), keyword['doc'])

    do_k = do_keywords

    def complete_keywords(self, text, line, begin_idx, end_idx):
        """Complete keywords command."""
        if len(line.split()) == 2:
            command, lib_name = line.split()
            return match_libs(lib_name)
        elif len(line.split()) == 1 and line.endswith(' '):
            return [_.name for _ in get_libs()]
        return []

    complete_k = complete_keywords

    def do_docs(self, kw_name):
        """Get keyword documentation for individual keywords.

         d(ocs) [<keyword_name>]
        """

        for lib in get_libs():
            for keyword in get_lib_keywords(lib, long_format=True):
                if keyword['name'].lower() == kw_name.lower():
                    logger.console(keyword['doc'])
                    return

        print_error('< not find keyword', kw_name)

    do_d = do_docs
