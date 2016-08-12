# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst', 'r') as f:
    readme = f.read()

setup (
    name = 'netstorageapi',
    version = '1.1.4',
    description = 'Akamai Netstorage API for Python',
    long_description = readme,
    packages = ['akamai'],
    package_dir = {'akamai': 'akamai'},
    install_requires = [
        'requests'
    ],
    author = 'Astin Choi',
    author_email = 'asciineo@gmail.com',
    url = 'https://github.com/AstinCHOI/akamai-netstorage',
    license='Apache 2.0',
    classifiers=(
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
)