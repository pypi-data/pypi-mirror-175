# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdshoplib',
 'gdshoplib.apps',
 'gdshoplib.apps.finance',
 'gdshoplib.apps.marketing',
 'gdshoplib.apps.products',
 'gdshoplib.core',
 'gdshoplib.core.manager',
 'gdshoplib.packages',
 'gdshoplib.services',
 'gdshoplib.services.notion']

package_data = \
{'': ['*'],
 'gdshoplib': ['templates/*'],
 'gdshoplib.services': ['avito/*', 'ula/*', 'vk/*']}

install_requires = \
['notion-client>=1.0.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'twine>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'gdshoplib',
    'version': '0.1.9',
    'description': '',
    'long_description': '# Библиотека с наборами действий для использования в остальных инструментах\n\napps - Инкапсуляция технических действий в операции над доменами\n\nservice - Инкапсуляция действий над платформами\n\ncore - Инструменты, чтобы собрать приложение в единый инструмент\n\n# Roadmap\n\n[] Модуль для управления Notion\n[] Модуль для управления Avito\n[] Модуль для управления VK сообществом\n[] Получение информации о товарах из Notion\n',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
