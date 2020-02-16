#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='enigma',
    version='0.1.0',
    packages=find_packages(),
    py_modules = ['enigma'],
    author='Maciej Czarnota',
    author_email='maciek.czarnota@gmail.com',

    package_data={'': ['*.html', '*.js', '*.map', '.css', ]},
    include_package_data=True,

    description='Komunikator Internetowy z funkcją szyfrowania asymetrycznego',
    long_description=open('README.md').read(),
    setup_requires=['wheel'],
    install_requires=[
        "flask",
        "flask_login",
        "flask_wtf",
        "sqlalchemy",
        "cockroachdb",
        "psycopg2-binary",
        "flask_socketio",
        "eventlet"
    ],
)




