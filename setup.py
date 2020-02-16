from setuptools import setup, find_packages

setup(
    name='enigma',
    version='0.1.0',
    packages=find_packages(),
    author='Maciej Czarnota',
    author_email='maciek.czarnota@gmail.com',

    package_data={
        '': ['enigma.py']
    },
    include_package_data=True,

    # package_data={
    #     'enigma': ['forms/*', 'sql/*', 'static/*', 'templates/*', '__init__.py', 'enigma.py', 'README.md']
    # },
    # include_package_data=True,


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




