#!/usr/bin/env python

import io
import os
import re

from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.rst')).read()

install_requires = ['prompt-toolkit < 3']  # 3.0 is not compatible with py3.5
install_requires.append('robotframework >= 3.0')


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
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
    long_description=README,
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
    install_requires=install_requires,
    tests_require='pexpect',
    test_suite='DebugLibrary.tests.test_debuglibrary.suite',
    platforms=['Linux', 'Unix', 'Windows', 'MacOS X'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ],
)
