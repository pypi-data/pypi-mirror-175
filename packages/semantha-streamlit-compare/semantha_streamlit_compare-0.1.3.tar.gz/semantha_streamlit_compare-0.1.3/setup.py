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
    'version': '0.1.3',
    'description': 'This is the project for a streamlit component which uses semantha semantic compare.',
    'long_description': 'This is the project to build a demo application for semantha\'s capabilities with streamlit.\n\n## Usage:\n\nUsing the component is simple:\n\n```python\nfrom semantha_streamlit_compare.components.compare import SemanticCompare\n\ncompare = SemanticCompare()\ncompare.build_input(sentences=("First sentence", "Second sentence"))\n```',
    'author': 'thingsTHINKING GmbH',
    'author_email': 'github@thingsthinking.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
