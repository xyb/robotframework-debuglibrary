import os
import sys
import tempfile

from robot import run_cli

TEST_SUITE = b'''*** Settings ***
Library  DebugLibrary

** test cases **
RFDEBUG REPL
    debug
'''


def shell():
    """A standalone robotframework shell."""

    default_no_logs = '-l None -x None -o None -L None -r None'

    with tempfile.NamedTemporaryFile(prefix='robot-debug-',
                                     suffix='.robot',
                                     delete=False) as test_file:
        test_file.write(TEST_SUITE)
        test_file.flush()

        if len(sys.argv) > 1:
            args = sys.argv[1:] + [test_file.name]
        else:
            args = default_no_logs.split() + [test_file.name]

        try:
            sys.exit(run_cli(args))
        finally:
            test_file.close()
            # pybot will raise PermissionError on Windows NT or later
            # if NamedTemporaryFile called with `delete=True`,
            # deleting test file seperated will be OK.
            if os.path.exists(test_file.name):
                os.unlink(test_file.name)


if __name__ == "__main__":
    # Usage: python -m DebugLibrary.shell
    shell()
