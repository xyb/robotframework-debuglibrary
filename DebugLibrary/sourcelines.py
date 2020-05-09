from robot.version import get_version

ROBOT_VERION_RUNNER_GET_STEP_LINENO = '3.2'


class RobotNeedUpgrade(Exception):
    """Need upgrade robotframework."""


def check_version():
    if get_version() < ROBOT_VERION_RUNNER_GET_STEP_LINENO:
        raise RobotNeedUpgrade


def print_source_lines(source_file, lineno, before_and_after=5):
    check_version()

    if not source_file or not lineno:
        return

    lines = open(source_file).readlines()
    start_index = max(1, lineno - before_and_after - 1)
    end_index = min(len(lines) + 1, lineno + before_and_after)
    _print_lines(lines, start_index, end_index, lineno)


def print_test_case_lines(source_file, lineno):
    check_version()

    if not source_file or not lineno:
        return

    lines = open(source_file).readlines()
    current_lineno = lineno

    # find the first line of current test case
    line_index = current_lineno - 1
    while line_index >= 0:
        line_index -= 1
        line = lines[line_index]
        if not _inside_test_case_block(line):
            break
    start_index = line_index

    # find the last line of current test case
    line_index = current_lineno - 1
    while line_index < len(lines):
        line = lines[line_index]
        if not _inside_test_case_block(line):
            break
        line_index += 1
    end_index = line_index

    _print_lines(lines, start_index, end_index, lineno)


def _inside_test_case_block(line):
    if line.startswith('#'):
        return True
    elif line.startswith(' '):
        return True
    elif line.startswith('\t'):
        return True
    return False


def _print_lines(lines, start_index, end_index, current_lineno):
    display_lines = lines[start_index:end_index]
    for lineno, line in enumerate(display_lines, start_index + 1):
        current_line_sign = ''
        if lineno == current_lineno:
            current_line_sign = '->'
        print('{:>3} {:2}\t{}'.format(lineno,
                                      current_line_sign,
                                      line.rstrip()))
