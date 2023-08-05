# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['askit']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.25.0,<0.26.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ask = askit.main:app']}

setup_kwargs = {
    'name': 'askit',
    'version': '0.1.3',
    'description': '',
    'long_description': '# AskAI\n\nAsk OpenAI your question from the command line and get a response. Super janky right now.\n\n# Installation\npip install pip install git+https://this-url\n\n# How to use:\nSet your api with command "ask api "your open api key here".\nThen ask questions with "ask it "your question here?"\nMake sure to finish the question with a question mark.',
    'author': 'Phil Harper',
    'author_email': 'phil@imrge.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
