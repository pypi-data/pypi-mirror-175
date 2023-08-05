# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0', 'typer[all]>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['ppm = src.main:app']}

setup_kwargs = {
    'name': 'ppm-cli',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'markus',
    'author_email': 'datamastery87@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
