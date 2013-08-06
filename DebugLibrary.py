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

from robot.errors import HandlerExecutionFailed
from robot.libraries.BuiltIn import BuiltIn
import cmd
import os
import re
import readline
import sys

__version__ = '0.3'

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

        print 'Exit the interpreter.'
        print 'You can also use the Ctrl-D shortcut.'

    do_EOF = do_exit
    help_EOF = help_exit

    def help_help(self):
        '''Help of Help command'''

        print 'Show help message.'


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

        print 'import library  SeleniumLibrary'
        self.rf_bi.run_keyword('import library', 'SeleniumLibrary')
        print 'start selenium server'
        self.rf_bi.run_keyword('start selenium server')
        self.rf_bi.run_keyword('sleep', '2')
        if arg:
            url = arg
        else:
            url = 'http://www.google.com/'
        print 'open browser  %s' % url
        self.rf_bi.run_keyword('open browser', url)

    def help_selenium(self):
        '''Help of Selenium command'''
        print 'Start a selenium server, and open google.com or other url in browser.'

    def default(self, line):
        '''Run RobotFramework keywords'''
        command = line.strip()
        if not command:
            return
        try:
            keyword = KEYWORD_SEP.split(command)
            result = self.rf_bi.run_keyword(*keyword)
            if result:
                print '< ', repr(result)
        except HandlerExecutionFailed, exc:
            print '< keyword: ', command
            print '! ', exc.full_message
        except Exception, exc:
            print '< keyword: ', command
            print '! FAILED: ', repr(exc)


class DebugLibrary(object):
    '''Debug Library for RobotFramework'''

    def debug(self):
        '''Open a interactive shell, run any RobotFramework keywords,
        seperated by two space or one tab, and Ctrl-D to exit.'''

        # re-wire stdout so that we can use the cmd module and have readline support
        old_stdout = sys.stdout
        sys.stdout = sys.__stdout__
        print '\n>>>>> Enter interactive shell, only accepted plain text format keyword.'
        debug_cmd = DebugCmd()
        debug_cmd.cmdloop()
        print '\n>>>>> Exit shell.'
        # put stdout back where it was
        sys.stdout = old_stdout


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
