# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['retry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'retry-extended',
    'version': '0.1.1',
    'description': 'Retry API compatible extended library',
    'long_description': '# Retry Extended\n[![Lint](https://github.com/strollby/retry-extended/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/strollby/retry-extended/actions/workflows/lint.yml)\n[![Test Package](https://github.com/strollby/retry-extended/actions/workflows/test.yml/badge.svg)](https://github.com/strollby/retry-extended/actions/workflows/test.yml)\n\n\n\nRetry API compatible maintained project\n',
    'author': 'Strollby Developers',
    'author_email': 'backend.developers@strollby.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/strollby/retry-extended',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
