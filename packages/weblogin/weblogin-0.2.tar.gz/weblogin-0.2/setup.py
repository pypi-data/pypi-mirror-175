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
    'version': '0.2',
    'description': 'Automates logging into web UIs to access unofficial APIs',
    'long_description': '# weblogin\n\n`weblogin` is a Python package that allows transparent logging in to web UIs to \naccess their unofficial APIs.\n\n`/doc` contains the source for the documented source code.\n\n`/src` contains the literate package source. Must be compiled to Python code \nusing NOWEB. Simply run `make`.\n\n`/tests` contains tests. Run `make` in that directory to run them.\n',
    'author': 'Daniel Bosk',
    'author_email': 'dbosk@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbosk/weblogin',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
