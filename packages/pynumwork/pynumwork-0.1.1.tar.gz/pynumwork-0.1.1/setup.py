# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pynumwork']
setup_kwargs = {
    'name': 'pynumwork',
    'version': '0.1.1',
    'description': 'A Python module that is created for solving simple math problems',
    'long_description': '',
    'author': 'spacecultengineer',
    'author_email': 'spacecultengineer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
