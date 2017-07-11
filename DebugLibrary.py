#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Xie Yanbo <xieyanbo@gmail.com>
# Author: Louie Lu <louie.lu@hopebaytech.com>
# This software is licensed under the New BSD License. See the LICENSE
# file in the top distribution directory for the full license text.

'''A debug library for RobotFramework, which can be used as an interactive
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
'''

from __future__ import print_function
from robot.errors import HandlerExecutionFailed
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from robot.variables import is_var
import cmd
import os
import re
import sys
try:
    import readline
except ImportError:
    # this will fail on IronPython
    pass
import sys

__version__ = '0.8'

KEYWORD_SEP = re.compile('  +|\t')


class BaseCmd(cmd.Cmd):

    '''Basic REPL tool'''

    def emptyline(self):
        '''By default Cmd runs last command if an empty line is entered.
        Disable it.'''

        pass

    def do_exit(self, arg):
        '''Exit'''

        return True

    def help_exit(self):
        '''Help of Exit command'''

        print('Exit the interpreter.')
        print('You can also use the Ctrl-D shortcut.')

    do_EOF = do_exit
    help_EOF = help_exit

    def help_help(self):
        '''Help of Help command'''

        print('Show help message.')


class DebugCmd(BaseCmd):

    '''Interactive debug shell'''

    use_rawinput = True
    prompt = '> '

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        BaseCmd.__init__(self, completekey, stdin, stdout)
        self.rf_bi = BuiltIn()

    def postcmd(self, stop, line):
        '''run after a command'''
        return stop

    def do_selenium(self, arg):
        '''initialized selenium environment, a shortcut for web test'''

        print('import library  Selenium2Library')
        self.rf_bi.run_keyword('import library', 'Selenium2Library')

        # Set defaults, overriden if args set
        url = 'http://www.google.com/'
        browser = 'firefox'
        if arg:
            args = KEYWORD_SEP.split(arg)
            if len(args) == 2:
                url, browser = args
            else:
                url = arg

        print('open browser  %s  %s' % (url, browser))
        self.rf_bi.run_keyword('open browser', url, browser)

    def help_selenium(self):
        '''Help of Selenium command'''
        print('Start a selenium 2 webdriver and open google.com '
              'or other url in firefox or other browser you expect.')
        print('selenium  [<url>]  [<browser>]')

    def default(self, line):
        '''Run RobotFramework keywordrun_clirun_clis'''
        command = line.strip()

        if not command:
            return
        try:
            u_command=''
            if sys.version_info > (3,):
                u_command = command
            else:
                u_command = command.decode("utf-8")
            keyword = KEYWORD_SEP.split(u_command)
            variable_name = keyword[0].rstrip('= ')

            if is_var(variable_name):
                variable_value = self.rf_bi.run_keyword(*keyword[1:])
                self.rf_bi._variables.__setitem__(variable_name,
                                                  variable_value)
                print('< ', variable_name, '=', repr(variable_value))
            else:
                result = self.rf_bi.run_keyword(*keyword)
                if result:
                    print('< ', repr(result))
        except HandlerExecutionFailed as exc:
            print('< keyword: %s' % command)
            print('! %s' % exc.full_message)
        except Exception as exc:
            print('< keyword: %s' % command)
            print('! FAILED: %s' % repr(exc))


class DebugLibrary(object):

    '''Debug Library for RobotFramework'''

    def debug(self):
        '''Open a interactive shell, run any RobotFramework keywords,
        seperated by two space or one tab, and Ctrl-D to exit.'''

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
        s = BuiltIn().get_library_instance('Selenium2Library')
        url = s._current_browser().command_executor._url

        return url

    def get_session_id(self):
        s = BuiltIn().get_library_instance('Selenium2Library')
        job_id = s._current_browser().session_id

        return job_id

    def get_webdriver_remote(self):
        remote_url = self.get_remote_url()
        session_id = self.get_session_id()

        s = 'from selenium import webdriver;' \
            'd=webdriver.Remote(command_executor="%s",' \
            'desired_capabilities={});' \
            'd.session_id="%s"' % (
                remote_url,
                session_id
            )

        logger.console("\nDEBUG FROM CONSOLE\n%s\n" % (s))
        logger.info(s)

        return s


def shell():
    '''A standalone robotframework shell'''

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

    args = '-l None -x None -o None -L None ' + source.name
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
