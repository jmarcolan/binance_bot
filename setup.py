from setuptools import setup
from setuptools import find_packages

setup(name='binance_bot',
    version='0.2',
    description='Grid binance bot',
    url='#',
    author='jmarcolan',
    author_email='jmarcolan@gmail.com',
    license='MIT',
    packages=find_packages(
        # All keyword arguments below are optional:
        # where='app'  # '.' by default
        # include=['mypackage*'],  # ['*'] by default
        # exclude=['mypackage.tests'],  # empty by default
    ),
    install_requires=[         
        'binance-connector',
        'sqlalchemy'],
    zip_safe=False)