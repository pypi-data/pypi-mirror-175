# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wotoplatform',
 'wotoplatform.types',
 'wotoplatform.types.base_types',
 'wotoplatform.types.data_types',
 'wotoplatform.types.errors',
 'wotoplatform.types.woto_crypto',
 'wotoplatform.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2', 'pysocks>=1.7.1']

setup_kwargs = {
    'name': 'wotoplatform',
    'version': '0.0.20',
    'description': '',
    'long_description': '\n### python library for woto-platform\n',
    'author': 'AliWoto',
    'author_email': 'woto@kaizoku.cyou',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ALiwoto/wotoplatform-Py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
