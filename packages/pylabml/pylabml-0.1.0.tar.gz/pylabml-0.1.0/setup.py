# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylabml']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0', 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'pylabml',
    'version': '0.1.0',
    'description': 'AI assisted data labelling with Python',
    'long_description': None,
    'author': 'Jaume Ferrarons',
    'author_email': 'jaume.ferrarons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
