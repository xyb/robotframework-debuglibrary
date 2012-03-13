#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Xie Yanbo <xieyanbo@gmail.com>
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
< '2011-10-13 18:50:31'
> import library  String
> get substring  helloworld  5  8
< 'wor'
> selenium  http://www.douban.com/
import library  SeleniumLibrary
start selenium server
open browser  http://www.douban.com/
> Ctrl-D
>>>>> Exit shell.
'''

import cmd
import re
import sys

# FIXME: why readline does not work?
#import readline
#readline.parse_and_bind('tab: complete')
#readline.parse_and_bind('set editing-mode emacs')

from robot.errors import HandlerExecutionFailed
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.2.3'

KEYWORD_SEP = re.compile('  |\t')

def output(*strings):
    '''Output strings to console

    RobotFramework captured stdout and stderr, only __stdout__ works.
    '''
    for arg in strings:
        sys.__stdout__.write(arg)

class BaseCmd(cmd.Cmd):
    '''Basic REPL tool'''

    def emptyline(self):
        '''By default Cmd run last command if an empty line is entered.
        Disable it.'''

        pass

    def do_exit(self, arg):
        '''Exit'''

        return True

    def help_exit(self):
        '''Help of Exit command'''

        self.stdout.write('Exit the interpreter.\n')
        self.stdout.write('You can also use the Ctrl-D shortcut.\n')

    do_EOF = do_exit
    help_EOF = help_exit

    def help_help(self):
        '''Help of Help command'''

        self.stdout.write('Show help message.\n')

class DebugCmd(BaseCmd):
    '''Interactive debug shell'''

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        '''Becase raw_input using sys.stdout that RobotFramework captured,
        the prompt of Cmd is missing unless use the __stdout__'''

        BaseCmd.__init__(self, completekey, stdin, stdout)
        self.stdout = sys.__stdout__
        self.prompt = ''
        self.use_rawinput = True
        self.rf_bi = BuiltIn()

    def postcmd(self, stop, line):
        '''run after a command'''

        # print prompt
        self.stdout.write('> ')
        return stop

    def do_selenium(self, arg):
        '''initialized selenium environment, a shortcut for web test'''

        self.stdout.write('import library  SeleniumLibrary\n')
        self.rf_bi.run_keyword('import library', 'SeleniumLibrary')
        self.stdout.write('start selenium server\n')
        self.rf_bi.run_keyword('start selenium server')
        self.rf_bi.run_keyword('sleep', '2')
        if arg:
            url = arg
        else:
            url = 'http://www.google.com/'
        self.stdout.write('open browser  %s\n' % url)
        self.rf_bi.run_keyword('open browser', url)

    def help_selenium(self):
        '''Help of Selenium command'''

        self.stdout.write('Start a selenium server, ')
        self.stdout.write('and open google.com or other url in browser.\n')

    def default(self, line):
        '''Run RobotFramework keywords'''

        command = line.strip()
        if not command:
            return
        try:
            keyword = KEYWORD_SEP.split(command)
            result = self.rf_bi.run_keyword(*keyword)
            if result:
                output('< ', repr(result), '\n')
        except HandlerExecutionFailed, exc:
            output('< keyword: ', command, '\n')
            output('! ', exc.full_message, '\n')
        except Exception, exc:
            output('< keyword: ', command, '\n')
            output('! FAILED: ', repr(exc), '\n')

class DebugLibrary(object):
    '''Debug Library for RobotFramework'''

    def debug(self):
        '''Open a interactive shell, run any RobotFramework keywords,
        seperated by two space or one tab, and Ctrl-D to exit.'''

        output('\n>>>>> Enter interactive shell, ')
        output('only accepted plain text format keyword.\n')
        debug_cmd = DebugCmd()
        debug_cmd.stdout.write('> ') # the first prompt
        debug_cmd.cmdloop()
        output('\n>>>>> Exit shell.\n')

def shell():
    '''A standalone robotframework shell'''

    import tempfile
    # ceate test suite file for REPL.
    source = tempfile.NamedTemporaryFile(prefix='robot_debug',
            suffix='.txt', delete=False)
    source.write('''*** Settings ***
Library  DebugLibrary

** test case **
REPL
    debug
''')
    source.flush()

    import robot
    import robot.runner
    args = '-l None -x None -o None -L None ' + source.name
    rc = robot.run_from_cli(args.split(), robot.runner.__doc__)
    sys.exit(rc)
    source.close()
    import os
    if os.path.exists(source.name):
        os.unlink(source.name)

if __name__ == '__main__':
    shell()
