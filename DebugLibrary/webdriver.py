from robot.api import logger

from .robotapp import get_robot_instance


def get_remote_url():
    """Get selenium URL for connecting to remote WebDriver."""
    se = get_robot_instance().get_library_instance('Selenium2Library')
    url = se._current_browser().command_executor._url

    return url


def get_session_id():
    """Get selenium browser session id."""
    se = get_robot_instance().get_library_instance('Selenium2Library')
    job_id = se._current_browser().session_id

    return job_id


def get_webdriver_remote():
    """Print the way connecting to remote selenium server."""
    remote_url = get_remote_url()
    session_id = get_session_id()

    code = 'from selenium import webdriver;' \
        'd=webdriver.Remote(command_executor="%s",' \
        'desired_capabilities={});' \
        'd.session_id="%s"' % (
            remote_url,
            session_id,
        )

    logger.console('''
DEBUG FROM CONSOLE
# geckodriver user please check https://stackoverflow.com/a/37968826/150841
%s
''' % (code))
    logger.info(code)

    return code
