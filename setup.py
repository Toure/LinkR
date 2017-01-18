#!/usr/bin/env python
# coding=utf-8
"""A setuptools-based script for installing Betelgeuse."""
from setuptools import setup, find_packages


with open('README.md') as handle:
    LONG_DESCRIPTION = handle.read()

with open('VERSION') as handle:
    VERSION = handle.read().strip()

setup(
    name='LinkR',
    author='Toure Dunnon',
    author_email='toure@redhat.com',
    version=VERSION,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    description=('junit generator to produce jenkins results xml reports'
                 'for polarion.'),
    include_package_data=True,
    license='Apache',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={'': ['LICENSE', 'settings.yaml']},
    url='https://github.com/Toure/LinkR',
    entry_points={
        'console_scripts': [
            'linkr = linkr.main:main'
        ]
    },
)
