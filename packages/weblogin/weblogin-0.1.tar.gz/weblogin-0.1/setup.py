# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['weblogin']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'weblogin',
    'version': '0.1',
    'description': 'Automates logging into web UIs to access unofficial APIs',
    'long_description': None,
    'author': 'Daniel Bosk',
    'author_email': 'dbosk@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
