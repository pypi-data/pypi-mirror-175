# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanist']

package_data = \
{'': ['*'], 'pyanist': ['dictionaries/*', 'word-frequency-lists/*']}

install_requires = \
['keyboard>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'pyanist',
    'version': '0.1.1',
    'description': 'Pyanist allows using chorded typing in addition to normal typing in order to improve your typing speed',
    'long_description': '# Pyanist\n\nPyanist is a tool that allows chorded typing using a regular N-key rollover keyboard.\nIt allows you to use chorded typing in addition to normal typing, which means that you can\nget started by chording a few frequent words instead of having to learn a whole system \nfrom scratch.\n\n\n# Attributions/sources\n\n./word-freq-top5000.csv - https://raw.githubusercontent.com/filiph/english_words/master/data/word-freq-top5000.csv (MIT)\n\n\n\n',
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
