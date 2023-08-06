# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beam', 'beam.configs', 'beam.scripts', 'beam.templates', 'beam.tests']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow-dataclass>=8.5.9,<9.0.0',
 'marshmallow==3.18.0',
 'mypy>=0.981,<0.982',
 'packaging>=21.3,<22.0',
 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'beam-sdk',
    'version': '0.9.6',
    'description': '',
    'long_description': 'None',
    'author': 'luke lombardi',
    'author_email': 'luke@slai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
