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

    with open(source_file) as f:
        lines = f.readlines()

    start_index = max(1, lineno - before_and_after - 1)
    end_index = min(len(lines) + 1, lineno + before_and_after)
    _print_lines(lines, start_index, end_index, lineno)


def print_test_case_lines(source_file, current_lineno):
    check_version()

    if not source_file or not current_lineno:
        return

    with open(source_file) as f:
        lines = f.readlines()

    # find the first line of current test case
    start_index = _find_first_lineno(lines, current_lineno)
    # find the last line of current test case
    end_index = _find_last_lineno(lines, current_lineno)

    _print_lines(lines, start_index, end_index, current_lineno)


def _find_last_lineno(lines, begin_lineno):
    line_index = begin_lineno - 1
    while line_index < len(lines):
        line = lines[line_index]
        if not _inside_test_case_block(line):
            break
        line_index += 1
    return line_index


def _find_first_lineno(lines, begin_lineno):
    line_index = begin_lineno - 1
    while line_index >= 0:
        line_index -= 1
        line = lines[line_index]
        if not _inside_test_case_block(line):
            break
    return line_index


def _inside_test_case_block(line):
    if line.startswith(' '):
        return True
    if line.startswith('\t'):
        return True
    if line.startswith('#'):
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
