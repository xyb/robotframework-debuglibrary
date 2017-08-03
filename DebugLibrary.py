#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Xie Yanbo <xieyanbo@gmail.com>
# Author: Louie Lu <louie.lu@hopebaytech.com>
# This software is licensed under the New BSD License. See the LICENSE
# file in the top distribution directory for the full license text.

"""A debug library for RobotFramework, which can be used as an interactive
shell(REPL) also.

As a library:
*** Settings ***
Library         DebugLibrary

** test case **
SOME TEST
    # some keywords...
    Debug

Run standalone:
$ python DebugLibrary.py
[...snap...]
>>>>> Enter interactive shell, only accepted plain text format keyword.
> log  hello
> get time
<  '2016-07-20 11:51:33'
> import library  String
> get substring  helloworld  5  8
< 'wor'
> ${secs} =  Get Time  epoch
<  ${secs} = 1474814470
> Log to console  ${secs}
1474814470
> selenium  https://www.google.com  chrome
import library  Selenium2Library
open browser  https://www.google.com  chrome
> close all browsers
> Ctrl-D
>>>>> Exit shell.
"""

from __future__ import print_function

import cmd
import os
import re
import sys

from robot.api import logger
from robot.errors import ExecutionFailed, HandlerExecutionFailed
from robot.libraries.BuiltIn import BuiltIn
from robot.variables import is_var

try:
    import readline  # noqa
except ImportError:
    # this will fail on IronPython
    pass

__version__ = '0.9.1'

KEYWORD_SEP = re.compile('  +|\t')


def get_command_line_encoding():
    encoding = ''
    try:
        encoding = sys.stdout.encoding
    except AttributeError:
        try:
            encoding = sys.__stdout__.encoding
        except Exception:
            pass
    return encoding or 'utf-8'


COMMAND_LINE_ENCODING = get_command_line_encoding()


class BaseCmd(cmd.Cmd):

    """Basic REPL tool"""

    def emptyline(self):
        """By default Cmd runs last command if an empty line is entered.
        Disable it."""

        pass

    def completedefault(self, text, line, begidx, endidx):
        return []

    def do_exit(self, arg):
        """Exit"""

        return True

    def help_exit(self):
        """Help of Exit command"""

        print('Exit the interpreter.')
        print('You can also use the Ctrl-D shortcut.')

    do_EOF = do_exit
    help_EOF = help_exit

    def help_help(self):
        """Help of Help command"""

        print('Show help message.')

    def do_pdb(self, arg):
        """Run python debugger pdb"""
        print('break into python debugger: pdb')
        import pdb
        pdb.set_trace()

    def help_pdb(self):
        """Help of pdb command"""
        print('pdb')
        print('Enter the python debuger pdb. For development only.')


def get_libs():
    """get libraries robotframework imported"""
    from robot.running.namespace import IMPORTER
    return sorted(IMPORTER._library_cache._items, key=lambda _: _.name)


def match_libs(name):
    libs = [_.name for _ in get_libs()]
    matched = [_ for _ in libs if _.lower().startswith(name.lower())]
    return matched


def run_keyword(bi, command):
    if not command:
        return
    try:
        u_command = ''
        if sys.version_info > (3,):
            u_command = command
        else:
            u_command = command.decode(COMMAND_LINE_ENCODING)
        keyword = KEYWORD_SEP.split(u_command)
        variable_name = keyword[0].rstrip('= ')

        if is_var(variable_name):
            variable_value = bi.run_keyword(*keyword[1:])
            bi._variables.__setitem__(variable_name,
                                      variable_value)
            print('< ', variable_name, '=', repr(variable_value))
        else:
            result = bi.run_keyword(*keyword)
            if result:
                print('< ', repr(result))
    except ExecutionFailed as exc:
        print('< keyword: %s' % command)
        print('! %s' % exc.message)
    except HandlerExecutionFailed as exc:
        print('< keyword: %s' % command)
        print('! %s' % exc.full_message)
    except Exception as exc:
        print('< keyword: %s' % command)
        print('! FAILED: %s' % repr(exc))


class DebugCmd(BaseCmd):

    """Interactive debug shell"""

    use_rawinput = True
    prompt = '> '

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        BaseCmd.__init__(self, completekey, stdin, stdout)
        self.rf_bi = BuiltIn()

    def postcmd(self, stop, line):
        """run after a command"""
        return stop

    def do_selenium(self, arg):
        """initialized selenium environment, a shortcut for web test"""

        command = 'import library  Selenium2Library'
        run_keyword(self.rf_bi, command)

        # Set defaults, overriden if args set
        url = 'http://www.google.com/'
        browser = 'firefox'
        if arg:
            args = KEYWORD_SEP.split(arg)
            if len(args) == 2:
                url, browser = args
            else:
                url = arg
        if '://' not in url:
            url = 'http://' + url

        command = 'open browser  %s  %s' % (url, browser)
        print(command)
        run_keyword(self.rf_bi, command)

    do_s = do_selenium

    def help_selenium(self):
        """Help of Selenium command"""
        print('s(elenium)  [<url>]  [<browser>]')
        print('Start a selenium 2 webdriver and open google.com '
              'or other url in firefox or other browser you expect.')

    help_s = help_selenium

    def complete_selenium(self, text, line, begidx, endidx):
        webdrivers = ['firefox',
                      'chrome',
                      'ie',
                      'opera',
                      'safari',
                      'phantomjs',
                      'remote']
        if len(line.split()) == 3:
            command, url, driver_name = line.lower().split()
            return [s for s in webdrivers if s.startswith(driver_name)]
        elif len(line.split()) == 2 and line.endswith(' '):
            return webdrivers
        return []

    complete_s = complete_selenium

    def default(self, line):
        """Run RobotFramework keywords"""
        command = line.strip()

        run_keyword(self.rf_bi, command)

    def do_libs(self, args):
        """Print libraries robotframework imported and builtin."""
        print('< Imported libraries:')
        for lib in get_libs():
            print('   {0} {1}'.format(lib.name, lib.version))
            if lib.doc:
                print('       {}'.format(lib.doc.split('\n')[0]))
            if '-s' in args:
                print('       {}'.format(lib.source))
        print('< Bultin libraries:')
        from robot.libraries import STDLIBS
        for name in sorted(list(STDLIBS)):
            print('   ', name)

    do_l = do_libs

    def help_libs(self):
        """Help of libs command"""
        print('l(ibs) [-s]')
        print('Print imported and builtin libraries, with source path')
        print('if `-s` specified.')

    help_l = help_libs

    def do_keywords(self, args):
        """Print keywords of RobotFramework libraries."""
        from robot.libdocpkg.robotbuilder import LibraryDocBuilder
        lib_name = args
        matched = match_libs(lib_name)
        if not matched:
            print('< not found library', lib_name)
            return
        for name in matched:
            print('< Keywords of library', name)
            lib = LibraryDocBuilder().build(name)
            for keyword in lib.keywords:
                print('   {0:<12s}\t{1}'.format(keyword.name,
                                                keyword.doc.split('\n')[0]))

    do_k = do_keywords

    def help_keywords(self):
        """Help of keywords command"""
        print('k(eywords) [<lib_name>]')
        print('Print keywords of libraries, all or starts with <lib_name>')

    help_k = help_keywords

    def complete_keywords(self, text, line, begidx, endidx):
        if len(line.split()) == 2:
            command, lib_name = line.split()
            return match_libs(lib_name)
        elif len(line.split()) == 1 and line.endswith(' '):
            return [_.name for _ in get_libs()]
        return []

    complete_k = complete_keywords


class DebugLibrary(object):

    """Debug Library for RobotFramework"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def debug(self):
        """Open a interactive shell, run any RobotFramework keywords.

        Keywords seperated by two space or one tab, and Ctrl-D to exit.
        """

        # re-wire stdout so that we can use the cmd module and have readline
        # support
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        print('\n>>>>> Enter interactive shell, only accepted plain text '
              'format keyword.')
        debug_cmd = DebugCmd()
        debug_cmd.cmdloop()
        print('\n>>>>> Exit shell.')
        # put stdout back where it was
        sys.stdout = old_stdout

    def get_remote_url(self):
        """Get selenium URL for connecting to remote WebDriver."""
        s = BuiltIn().get_library_instance('Selenium2Library')
        url = s._current_browser().command_executor._url

        return url

    def get_session_id(self):
        """Get selenium browser session id."""
        s = BuiltIn().get_library_instance('Selenium2Library')
        job_id = s._current_browser().session_id

        return job_id

    def get_webdriver_remote(self):
        """Print the way connecting to remote selenium server."""
        remote_url = self.get_remote_url()
        session_id = self.get_session_id()

        s = 'from selenium import webdriver;' \
            'd=webdriver.Remote(command_executor="%s",' \
            'desired_capabilities={});' \
            'd.session_id="%s"' % (
                remote_url,
                session_id
            )

        logger.console('''
DEBUG FROM CONSOLE
# geckodriver user please check https://stackoverflow.com/a/37968826/150841
%s
''' % (s))
        logger.info(s)

        return s


def shell():
    """A standalone robotframework shell"""

    import tempfile
    # ceate test suite file for REPL.
    source = tempfile.NamedTemporaryFile(prefix='robot_debug',
                                         suffix='.txt', delete=False)
    source.write(b'''*** Settings ***
Library  DebugLibrary

** test case **
REPL
    debug
''')
    source.flush()

    args = '-l None -x None -o None -L None -r None ' + source.name
    import robot
    try:
        from robot import run_cli
        rc = run_cli(args.split())
    except ImportError:
        import robot.runner
        rc = robot.run_from_cli(args.split(), robot.runner.__doc__)

    source.close()
    if os.path.exists(source.name):
        os.unlink(source.name)
    sys.exit(rc)


if __name__ == '__main__':
    shell()
