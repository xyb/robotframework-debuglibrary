#!/usr/bin/env python

import sys
import os
from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()
PY3 = sys.version_info[0] == 3

install_requires = []
if PY3:
    install_requires.append('robotframework-python3 >= 2.8')
else:
    install_requires.append('robotframework >= 2.8')

setup(
    name = 'robotframework-debuglibrary',
    version = '0.5',
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
    install_requires = install_requires,
    platforms = ['Linux', 'Unix', 'Windows', 'MacOS X'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ],
)
