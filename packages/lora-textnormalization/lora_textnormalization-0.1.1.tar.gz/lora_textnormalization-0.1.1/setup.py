# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lora_textnormalization']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'lora-textnormalization',
    'version': '0.1.1',
    'description': 'A text normalization package for general English NLP tasks.',
    'long_description': '# import\n\n`from lora_textnormalization import spacy_process`\n\n# Usage\n\n`normalized = spacy_process("Markov\'s long text")`\n\n# Output\n\n`list[\'Markov\', \'long\', \'text\']`\n',
    'author': 'Adrian-Wong',
    'author_email': 'adrian@asklora.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
