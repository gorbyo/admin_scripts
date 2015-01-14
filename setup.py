#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name='admin_scripts',
    version='0.0.1',
    description='Short description',
    long_description=''.join(open('README.rst').readlines()),
    keywords='http, check',
    author='Oleh Horbachov',
    author_email='gorbyo@gmail.com',
    license='GPLv2',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ],
    requires=['requests', ]
)
