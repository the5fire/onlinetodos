# coding: utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='onlinetodos',
    version='${version}',
    description='',
    long_description=readme,
    author='the5fire',
    author_email='thefivefire@gmail.com',
    url='http://todos.the5fire.com',
    packages=find_packages(exclude=['*.pyc']),
    include_package_data = True,
    package_data = {
    },
    install_requires=[
        'web.py',
        'gunicorn',
        ],
    entry_points={
        'console_scripts': [
            'onlinetodos = src.server',
        ]
    },
)
