# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantha_streamlit_compare', 'semantha_streamlit_compare.components']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'semantha-streamlit-compare',
    'version': '0.1.0',
    'description': '',
    'long_description': "This is the project to build a demo application for semantha's capabilities with streamlit. ",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
