#!/usr/bin/env python
# coding=utf-8
"""A setuptools-based script for installing Betelgeuse."""
from setuptools import setup

with open('README.md') as handle:
    LONG_DESCRIPTION = handle.read()

with open('VERSION') as handle:
    VERSION = handle.read().strip()

setup(
    name='LinkR',
    author='Toure',
    author_email='toure@redhat.com',
    version=VERSION,
    py_modules=['betelgeuse'],
    install_requires=['', 'docutils','testimony'],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    description=('Wrapper for shell scripts to interface with '
                 'pylarion library which is a python based project.'),
    include_package_data=True,
    license='Apache',
    long_description=LONG_DESCRIPTION,
    package_data={'': ['LICENSE']},
    url='https://github.com/Toure/LinkR',
)
