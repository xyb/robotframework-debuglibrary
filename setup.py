#!/usr/bin/env python

import io
import os
import re

from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    with io.open(
        os.path.join(ROOT, *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='robotframework-debuglibrary',
    version=find_version('DebugLibrary/version.py'),
    description='RobotFramework debug library and an interactive shell',
    long_description=read('README.rst'),
    author='Xie Yanbo',
    author_email='xieyanbo@gmail.com',
    license='New BSD',
    packages=['DebugLibrary'],
    entry_points={
        'console_scripts': [
            'rfshell = DebugLibrary.shell:shell',
            'rfdebug = DebugLibrary.shell:shell',
        ],
    },
    zip_safe=False,
    url='https://github.com/xyb/robotframework-debuglibrary/',
    keywords='robotframework,debug,shell,repl',
    install_requires=[
        'prompt-toolkit >= 3',
        'robotframework >= 4',
    ],
    tests_require=['pexpect', 'coverage'],
    test_suite='tests.test_debuglibrary.suite',
    platforms=['Linux', 'Unix', 'Windows', 'MacOS X'],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Utilities',
    ],
)
