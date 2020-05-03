import re

from robot.api import logger
from robot.libdocpkg.model import LibraryDoc
from robot.libdocpkg.robotbuilder import KeywordDocBuilder, LibraryDocBuilder
from robot.libraries import STDLIBS
from robot.libraries.BuiltIn import BuiltIn
from robot.running.namespace import IMPORTER
from robot.running.signalhandler import STOP_SIGNAL_MONITOR

from .utils import memoize

try:
    from robot.variables.search import is_variable
except ImportError:
    from robot.variables import is_var as is_variable  # robotframework < 3.2

KEYWORD_SEP = re.compile('  +|\t')

SELENIUM_WEBDRIVERS = ['firefox', 'chrome', 'ie',
                       'opera', 'safari', 'phantomjs', 'remote']


def get_robot_instance():
    """Get robotframework builtin instance as context."""
    return BuiltIn()


def get_builtin_libs():
    """Get robotframework builtin library names."""
    return list(STDLIBS)


def get_libs():
    """Get imported robotframework library names."""
    return sorted(IMPORTER._library_cache._items, key=lambda _: _.name)


def get_libs_dict():
    """Get imported robotframework libraries as a name -> lib dict"""
    return {lib.name: lib for lib in IMPORTER._library_cache._items}


def match_libs(name=''):
    """Find libraries by prefix of library name, default all"""
    libs = [_.name for _ in get_libs()]
    matched = [_ for _ in libs if _.lower().startswith(name.lower())]
    return matched


class ImportedLibraryDocBuilder(LibraryDocBuilder):

    def build(self, lib):
        libdoc = LibraryDoc(
            name=lib.name,
            doc=self._get_doc(lib),
            doc_format=lib.doc_format,
        )
        libdoc.inits = self._get_initializers(lib)
        libdoc.keywords = KeywordDocBuilder().build_keywords(lib)
        return libdoc


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


def parse_keyword(command):
    """Split a robotframework keyword string."""
    return KEYWORD_SEP.split(command)


def reset_robotframework_exception():
    """Resume RF after press ctrl+c during keyword running."""
    if STOP_SIGNAL_MONITOR._signal_count:
        STOP_SIGNAL_MONITOR._signal_count = 0
        STOP_SIGNAL_MONITOR._running_keyword = True
        logger.info('Reset last exception of DebugLibrary')


def assign_variable(robot_instance, variable_name, args):
    """Assign a robotframework variable."""
    variable_value = robot_instance.run_keyword(*args)
    robot_instance._variables.__setitem__(variable_name, variable_value)
    return variable_value


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


def start_selenium_commands(arg):
    """Start a selenium webdriver and open url in browser you expect.

    arg:  [<url> or google]  [<browser> or firefox]
    """
    yield 'import library  SeleniumLibrary'

    # Set defaults, overriden if args set
    url = 'http://www.google.com/'
    browser = 'firefox'
    if arg:
        args = parse_keyword(arg)
        if len(args) == 2:
            url, browser = args
        else:
            url = arg
    if '://' not in url:
        url = 'http://' + url

    yield 'open browser  %s  %s' % (url, browser)
