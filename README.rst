Debug Library for Robot Framework
=================================

.. contents::
   :local:

Introduction
------------

Robotframework-DebugLibrary is a debug library for `RobotFramework`_,
which can be used as an interactive shell(REPL) also.

.. _`RobotFramework`: http://robotframework.org/

Installation
------------

To install using ``pip``::

    pip install robotframework-debuglibrary


Usage
-----

You can use this as a library, import ``DebugLibrary`` and call ``Debug``
keyword in your test files like this::

    *** Settings ***
    Library         DebugLibrary

    ** test case **
    SOME TEST
        # some keywords...
        Debug

Or you can run it standalone as a ``RobotFramework`` shell::

    $ rfdebug
    [...snap...]
    >>>>> Enter interactive shell, only accepted plain text format keyword.
    > help
    Input Robotframework keywords, or commands listed below.
    Use "libs" or "l" to see available libraries,
    use "keywords" or "k" to see list of library keywords,
    use the TAB keyboard key to auto complete keywords.

    Documented commands (type help <topic>):
    ========================================
    EOF  exit  help  k  keywords  l  libs  pdb  s  selenium

    > log  hello
    > get time
    < '2011-10-13 18:50:31'
    > import library  String
    > get substring  helloworld  5  8
    < 'wor'
    > ${secs} =  Get Time  epoch
    # ${secs} = 1474814470
    > Log to console  ${secs}
    1474814470
    > @{list} =  Create List    hello    world
    # @{list} = ['hello', 'world']
    > Log to console  ${list}
    ['hello', 'world']
    > &{dict} =  Create Dictionary    name=admin    email=admin@test.local
    # &{dict} = {'name': 'admin', 'email': 'admin@test.local'}
    > Log  ${dict.name}
    > help selenium
    Start a selenium 2 webdriver and open url in browser you expect.

            s(elenium)  [<url>]  [<browser>]

            default url is google.com, default browser is firefox.
    > selenium  google.com  chrome
    # import library  Selenium2Library
    # open browser  http://google.com  chrome
    < 1
    > close all browsers
    > Ctrl-D
    >>>>> Exit shell.

The interactive shell support auto completion for robotframework keywords and
commands. The history will save at ``~/.rfdebug_history`` default, or any file
defined in environment variable ``RFDEBUG_HISTORY``.

Submitting issues
-----------------

Bugs and enhancements are tracked in the `issue tracker
<https://github.com/xyb/robotframework-debuglibrary/issues>`_.

Before submitting a new issue, it is always a good idea to check is the
same bug or enhancement already reported. If it is, please add your comments
to the existing issue instead of creating a new one.

License
-------

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
