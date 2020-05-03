
from .robotkeyword import parse_keyword

SELENIUM_WEBDRIVERS = ['firefox', 'chrome', 'ie',
                       'opera', 'safari', 'phantomjs', 'remote']


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
