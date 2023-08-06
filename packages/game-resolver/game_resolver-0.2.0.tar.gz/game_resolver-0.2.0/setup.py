# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['game_resolver', 'game_resolver.games', 'game_resolver.util']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'game-resolver',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'nariaki-nishino',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
