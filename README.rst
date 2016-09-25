Introduction
============

Robotframework-DebugLibrary is A debug library for `RobotFramework`_, which can be used as an interactive shell(REPL) also.

.. _`RobotFramework`: http://robotframework.org/

Installation
============

Installation is done just as for any other Python library. Using the ``pip`` or
``easy_install`` command from setuptools is the easiest.

To install using ``pip``::

    pip install robotframework-debuglibrary

To install using ``easy_install``::

    easy_install robotframework-debuglibrary

Usage
=====

You can use this as a library, import ``DebugLibrary`` and call ``Debug`` keyword in your test files like this::

    *** Settings ***
    Library         DebugLibrary

    ** test case **
    SOME TEST
        # some keywords...
        Debug

Or you can run it standalone as a ``RobotFramework`` shell::

    $ rfshell
    [...snap...]
    >>>>> Enter interactive shell, only accepted plain text format keyword.
    > log  hello
    > get time
    <  '2011-10-13 18:50:31'
    > import library  String
    > get substring  helloworld  5  8
    < 'wor'
    > ${secs} =  Get Time  epoch
    <  ${secs} = 1474814470
    > Log to console  ${secs}
    1474814470
    > @{list} =  Create List    hello    world
    <  @{list} = [u'hello', u'world']
    > Log to console  ${list}
    [u'hello', u'world']
    > &{dict} =  Create Dictionary    name=admin    email=admin@test.local
    <  &{dict} = {u'name': u'admin', u'email': u'admin@test.local'}
    > Log  ${dict.name}
    > help selenium
    Start a selenium 2 webdriver and open google.com or other url in firefox or other browser you expect.
    selenium  [<url>]  [<browser>]
    > selenium  http://www.google.com/  chrome
    import library  Selenium2Library
    open browser  http://www.google.com/  chrome
    > close all browsers
    > Ctrl-D
    >>>>> Exit shell.

License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
