# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_aio_pool']

package_data = \
{'': ['*']}

install_requires = \
['celery>=5,<6']

setup_kwargs = {
    'name': 'celery-aio-pool',
    'version': '0.1.0rc0',
    'description': 'Celery worker pool with support for asyncio coroutines as tasks',
    'long_description': '# Celery AsyncIO Pool\n\n![python](https://img.shields.io/pypi/pyversions/celery-aio-pool.svg)\n![version](https://img.shields.io/pypi/v/celery-aio-pool.svg)\n![downloads](https://img.shields.io/pypi/dm/celery-aio-pool.svg)\n![format](https://img.shields.io/pypi/format/celery-aio-pool.svg)\n\n![Logo](https://repository-images.githubusercontent.com/198568368/35298e00-c1e8-11e9-8bcf-76c57ee28db8)\n\n- Free software: GNU Affero General Public License v3+\n\n## Coming Soon™\n',
    'author': 'Mark S.',
    'author_email': 'the@wondersmithd.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/the-wondersmith/celery-aio-pool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
