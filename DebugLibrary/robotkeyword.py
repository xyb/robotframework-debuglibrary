import re

from robot.libraries.BuiltIn import BuiltIn

from .memoize import memoize
from .robotlib import ImportedLibraryDocBuilder, get_libs
from .robotvar import assign_variable

try:
    from robot.variables.search import is_variable
except ImportError:
    from robot.variables import is_var as is_variable  # robotframework < 3.2

KEYWORD_SEP = re.compile('  +|\t')


def parse_keyword(command):
    """Split a robotframework keyword string."""
    # TODO use robotframework functions
    return KEYWORD_SEP.split(command)


@memoize
def get_lib_keywords(library, long_format=False):
    """Get keywords of imported library."""
    lib = ImportedLibraryDocBuilder().build(library)
    keywords = []
    for keyword in lib.keywords:
        if long_format:
            doc = keyword.doc
        else:
            doc = keyword.doc.split('\n')[0]
        keywords.append({
            'name': keyword.name,
            'lib': library.name,
            'doc': doc,
        })
    return keywords


def get_keywords():
    """Get all keywords of libraries."""
    for lib in get_libs():
        yield from get_lib_keywords(lib)


def run_keyword(robot_instance, keyword):
    """Run a keyword in robotframewrk environment."""
    if not keyword:
        return

    keyword_args = parse_keyword(keyword)
    keyword = keyword_args[0]
    args = keyword_args[1:]

    is_comment = keyword.strip().startswith('#')
    if is_comment:
        return

    variable_name = keyword.rstrip('= ')
    if is_variable(variable_name):
        variable_only = not args
        if variable_only:
            display_value = ['Log to console', keyword]
            robot_instance.run_keyword(*display_value)
        else:
            variable_value = assign_variable(
                robot_instance,
                variable_name,
                args,
            )
            echo = '{0} = {1!r}'.format(variable_name, variable_value)
            return ('#', echo)
    else:
        output = robot_instance.run_keyword(keyword, *args)
        if output:
            return ('<', repr(output))


def run_debug_if(condition, *args):
    """Runs DEBUG if condition is true."""

    return BuiltIn().run_keyword_if(condition,
                                    'DebugLibrary.DEBUG',
                                    *args)
