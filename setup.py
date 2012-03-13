#!/usr/bin/env python

import os
from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()

setup(
    name = 'robotframework-debuglibrary',
    version = '0.2.3',
    description = 'RobotFramework debug library and an interactive shell',
    long_description = README,
    author = 'Xie Yanbo',
    author_email = 'xieyanbo@gmail.com',
    license = 'New BSD',
    packages = [],
    py_modules = ['DebugLibrary'],
    entry_points = {
        'console_scripts': [
            'rfshell = DebugLibrary:shell',
            ],
    },
    zip_safe = False,
    url = 'https://github.com/xyb/robotframework-debuglibrary/',
    keywords = 'robotframework,debug,shell,repl',
    install_requires = [
        'robotframework>=2.0',
        ],
    platforms = ['Linux', 'Unix', 'Windows', 'MacOS X'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ],
)
