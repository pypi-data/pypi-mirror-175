# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcapprox']

package_data = \
{'': ['*']}

install_requires = \
['cvxpy>=1.2.1,<2.0.0',
 'cvxpylayers>=0.1.5,<0.2.0',
 'numpy>=1.23.4,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'torch>=1.12.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'pcapprox',
    'version': '0.3.0',
    'description': 'A Python package for parameterized convex approximators',
    'long_description': 'None',
    'author': 'JinraeKim',
    'author_email': 'kjl950403@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
