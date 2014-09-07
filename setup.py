# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import re
from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()


def get_version():
    VERSIONFILE = 'bitstamp/__init__.py'
    initfile_lines = open(VERSIONFILE, 'rt').readlines()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in initfile_lines:
        mo = re.search(VSRE, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (VERSIONFILE,))

setup(
    name='bitstamp',
    version=get_version(),
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    zip_safe=False,
    description='Bitstamp API',
    url='https://bitbucket.org/socketubs/bitstamp',
    author='Geoffrey Lehée',
    author_email='hello@socketubs.org',
    install_requires=required,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
