"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'cryptowatch',
    version = '0.1.0.dev1',
    author = 'Aaron Stewart',
    author_email = 'aaron.a.stewart@gmail.com',
    license='MIT',
    url = 'https://github.com/astew/cryptowatch-python',
    packages = find_packages(),
    install_requires = ['requests>=2.5'],
    description = 'A python wrapper for accessing Cryptowat.ch\'s public REST API',
    download_url = 'https://github.com/astew/cryptowatch-python/archive/master.zip',
    keywords = ['cryptowatch', 'bitcoin', 'BTC', 'ethereum', 'ETH', 'client', 'api', 'wrapper', 'exchange', 'crypto', 'currency'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)