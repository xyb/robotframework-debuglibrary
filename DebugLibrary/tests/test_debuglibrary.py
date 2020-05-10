#!/usr/bin/env python

import unittest
from os.path import abspath, dirname, join

import pexpect
from robot.version import get_version

TIMEOUT_SECONDS = 2

child = None


def check_result(pattern):
    index = child.expect([pattern, pexpect.EOF, pexpect.TIMEOUT],
                         timeout=TIMEOUT_SECONDS)
    try:
        assert index == 0
    except AssertionError:
        print('\n==== Screen buffer raw ====\n',
              child._buffer.getvalue(),
              '\n^^^^ Screen buffer raw ^^^^')
        print('==== Screen buffer ====\n',
              child._buffer.getvalue().decode('utf8'),
              '\n^^^^ Screen buffer ^^^^')
        raise


def check_prompt(keys, pattern):
    child.write(keys)
    check_result(pattern)
    child.write('\003')  # ctrl-c: reset inputs


def check_command(command, pattern):
    child.sendline(command)
    check_result(pattern)


def base_functional_testing():
    global child
    child = pexpect.spawn('/usr/bin/env python -m DebugLibrary.shell')
    child.expect('Enter interactive shell', timeout=TIMEOUT_SECONDS * 3)

    # auto complete
    check_prompt('key\t',
                 'keywords')
    check_prompt('key\t',
                 'Keyword Should Exist')
    check_prompt('buil\t',
                 'Library: BuiltIn')
    check_prompt('builtin.\t',
                 'Call Method')
    check_prompt('get\t',
                 'Get Count')
    check_prompt('get\t',
                 'Get Time')

    # keyword
    check_command('log to console  hello',
                  'hello')
    check_command('get time',
                  '.*-.*-.* .*:.*:.*')
    check_prompt('g',
                 'et time')
    check_command('help keywords',
                  'Print keywords of libraries')
    check_command('k builtin',
                  'Sleep')
    check_command('d sleep',
                  'Pauses the test executed for the given time')

    # var
    check_command('@{{list}} =  Create List    hello    world',
                  "@{{list}} = ['helo', 'world']")
    check_command('${list}',
                  "['helo', 'world']")
    check_command('&{dict} =  Create Dictionary    name=admin',
                  "&{dict} = {'name': 'admin'}")
    check_command('${dict.name}',
                  'admin')

    # fail-safe
    check_command('fail',
                  'AssertionError')
    check_command('nothing',
                  "No keyword with name 'nothing' found.")

    return 'OK'


def step_functional_testing():
    global child
    path = join(dirname(abspath(__file__)), 'step.robot')
    child = pexpect.spawn('/usr/bin/env robot {}'.format(path))
    child.expect('Enter interactive shell', timeout=TIMEOUT_SECONDS * 3)

    check_command('list',
                  'Please run `step` or `next` command first.')

    support_source_lineno = get_version() >= '3.2'

    if support_source_lineno:
        check_command('s',  # step
                      '/DebugLibrary/tests/step.robot\(7\).*'
                      '-> log to console  working.*'
                      '=> BuiltIn.Log To Console  working')
        check_command('l',  # list
                      '  7 ->	    log to console  working')
        check_command('n',  # next
                      '/DebugLibrary/tests/step.robot\(8\).*'
                      '@.* =  Create List    hello    world.*'
                      '@.* = BuiltIn.Create List  hello  world')
        check_command('',  # just repeat last command
                      '/DebugLibrary/tests/step.robot\(11\).*'
                      '-> log to console  another test case.*'
                      '=> BuiltIn.Log To Console  another test case')
        check_command('l',  # list
                      '  6   	    debug.*'
                      '  7   	    log to console  working.*'
                      '  8   	    @.* =  Create List    hello    world.*'
                      '  9.*'
                      ' 10   	test2.*'
                      ' 11 ->	    log to console  another test case.*'
                      ' 12   	    log to console  end')
        check_command('ll',  # longlist
                      ' 10   	test2.*'
                      ' 11 ->	    log to console  another test case.*'
                      ' 12   	    log to console  end')
    else:
        check_command('s',  # step
                      '=> BuiltIn.Log To Console  working')
        check_command('l',  # list
                      'Please upgrade robotframework')
        check_command('n',  # next
                      '@.* = BuiltIn.Create List  hello  world')
        check_command('',  # repeat last command
                      '=> BuiltIn.Log To Console  another test case')

    # exit
    check_command('c',  # continue
                  'Exit shell.*'
                  'another test case.*'
                  'end')

    return 'OK'


class FunctionalTestCase(unittest.TestCase):
    def test_base_functional(self):
        assert base_functional_testing() == 'OK'

    def test_step_functional(self):
        assert step_functional_testing() == 'OK'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(FunctionalTestCase('test_base_functional'))
    suite.addTest(FunctionalTestCase('test_step_functional'))
    return suite


if __name__ == '__main__':
    print(base_functional_testing())
    print(step_functional_testing())
