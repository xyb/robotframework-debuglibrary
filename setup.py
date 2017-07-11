#!/usr/bin/env python

import io
import os
import re
import sys

from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()
PY3 = sys.version_info[0] == 3

install_requires = []
if PY3:
    install_requires.append('robotframework >= 3.0')
else:
    install_requires.append('robotframework >= 2.8')


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='robotframework-debuglibrary',
    version=find_version('DebugLibrary.py'),
    description='RobotFramework debug library and an interactive shell',
    long_description=README,
    author='Xie Yanbo',
    author_email='xieyanbo@gmail.com',
    license='New BSD',
    packages=[],
    py_modules=['DebugLibrary'],
    entry_points={
        'console_scripts': [
            'rfshell = DebugLibrary:shell',
        ],
    },
    zip_safe=False,
    url='https://github.com/xyb/robotframework-debuglibrary/',
    keywords='robotframework,debug,shell,repl',
    install_requires=install_requires,
    platforms=['Linux', 'Unix', 'Windows', 'MacOS X'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ],
)
