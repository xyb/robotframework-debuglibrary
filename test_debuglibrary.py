#!/usr/bin/env python

import unittest

import pexpect

TIMEOUT_SECONDS = 1


def functional_testing():
    child = pexpect.spawnu('/usr/bin/env python DebugLibrary.py')
    child.expect('Enter interactive shell', timeout=5)

    def check_prompt(keys, pattern):
        child.write(keys)
        index = child.expect([pattern, pexpect.EOF, pexpect.TIMEOUT],
                             timeout=TIMEOUT_SECONDS)
        assert index == 0
        child.write('\003')  # ctrl-c: reset inputs

    check_prompt('key\t', 'keywords')
    check_prompt('key\t', 'Keyword Should Exist')
    check_prompt('buil\t', 'Library: BuiltIn')
    check_prompt('builtin.\t', 'Call Method')
    check_prompt('get\t', 'Get Count')
    check_prompt('get\t', 'Get Time')

    def check_command(command, pattern):
        child.sendline(command)
        index = child.expect([pattern, pexpect.EOF, pexpect.TIMEOUT],
                             timeout=TIMEOUT_SECONDS)
        assert index == 0

    check_command('log to console  hello', 'hello')
    check_command('get time', '.*-.*-.* .*:.*:.*')
    check_prompt('g', 'et time')
    check_command('help keywords', 'Print keywords of libraries')
    check_command('help keywords', 'Print keywords of libraries')
    check_command('k builtin', 'Sleep')
    check_command('d sleep', 'Pauses the test executed for the given time')

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
