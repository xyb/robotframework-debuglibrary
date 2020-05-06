#!/usr/bin/env python

import unittest

import pexpect

TIMEOUT_SECONDS = 2


def functional_testing():
    child = pexpect.spawn('/usr/bin/env python -m DebugLibrary.shell')
    child.expect('Enter interactive shell', timeout=TIMEOUT_SECONDS * 3)

    def check_result(pattern):
        index = child.expect([pattern, pexpect.EOF, pexpect.TIMEOUT],
                             timeout=TIMEOUT_SECONDS)
        try:
            assert index == 0
        except AssertionError:
            print('Screen buffer: ', child._buffer.getvalue())
            raise

    def check_prompt(keys, pattern):
        child.write(keys)
        check_result(pattern)
        child.write('\003')  # ctrl-c: reset inputs

    def check_command(command, pattern):
        child.sendline(command)
        check_result(pattern)

    # auto complete
    check_prompt('key\t', 'keywords')
    check_prompt('key\t', 'Keyword Should Exist')
    check_prompt('buil\t', 'Library: BuiltIn')
    check_prompt('builtin.\t', 'Call Method')
    check_prompt('get\t', 'Get Count')
    check_prompt('get\t', 'Get Time')

    # keyword
    check_command('log to console  hello', 'hello')
    check_command('get time', '.*-.*-.* .*:.*:.*')
    check_prompt('g', 'et time')
    check_command('help keywords', 'Print keywords of libraries')
    check_command('k builtin', 'Sleep')
    check_command('d sleep', 'Pauses the test executed for the given time')

    # var
    check_command('@{{list}} =  Create List    hello    world',
                  "@{{list}} = ['helo', 'world']")
    check_command('${list}', "['helo', 'world']")
    check_command('&{dict} =  Create Dictionary    name=admin',
                  "&{dict} = {'name': 'admin'}")
    check_command('${dict.name}', 'admin')

    # fail-safe
    check_command('fail', 'AssertionError')
    check_command('nothing', "No keyword with name 'nothing' found.")

    return 'OK'


class FunctionalTestCase(unittest.TestCase):
    def test_functional(self):
        assert functional_testing() == 'OK'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(FunctionalTestCase('test_functional'))
    return suite


if __name__ == '__main__':
    print(functional_testing())
