# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aidd_codebase',
 'aidd_codebase.datamodules',
 'aidd_codebase.framework',
 'aidd_codebase.models',
 'aidd_codebase.models.modules',
 'aidd_codebase.new_project',
 'aidd_codebase.new_project.src',
 'aidd_codebase.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aidd-codebase',
    'version': '0.2.0',
    'description': 'High-level codebase for deep learning development in drug discovery.',
    'long_description': '# AIDD Codebase\n\n![PyPI](https://img.shields.io/pypi/v/aidd-codebase)\n![PyPI](https://img.shields.io/pypi/pyversions/aidd-codebase)\n![PyPI](https://img.shields.io/github/license/aidd-msca/aidd-codebase)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jlyEd1yxhvFCN82YqEFI82q2n0k_y06F?usp=sharing)\n\nA high-level codebase for deep learning development in drug discovery applications using PyTorch-Lightning.\n\n## Dependencies\n\nThe codebase requires the following additional dependencies\n- CUDA >= 11.4\n- PyTorch >= 1.9\n- Pytorch-Lightning >= 1.5 \n- RDKit \n- Optionally supports: tensorboard and/or wandb\n\n\n## Installation\n\nThe codebase can be installed from PyPI using `pip`, or your package manager of choice, with\n\n```bash\n$ pip install aidd-codebase\n```\n\n## Usage\n\n1. __*Configuration*__: The coding framework has a number of argument dataclasses in the file *arguments.py*. This file contains all standard arguments for each of the models. Because they are dataclasses, you can easily adapt them to your own needs. \n<br> \nDoes your Seq2Seq adaptation need an extra argument? Import the Seq2SeqArguments from arguments.py, create your own dataclass which inherits it and add your extra argument. <br> <br>\n*It is important to note that the order of supplying arguments to a script goes as follows:* <br>\n- --flags override config.yaml <br>\n- config.yaml overrides default values in arguments.py <br>\n- default values from arguments.py are used when no other values are supplied<br>\nAt the end, it stores all arguments in config.yaml\n<br><br>\n\n2. __*Use*__: The coding framework has four main parts: <br>\n- utils\n- data_utils\n- models\n- interpretation\n\nThese parts should be used \n&nbsp; \n\n3. __*File Setup*__: The setup of the files in the system is best used as followed:<br>\ncoding_framework<br> \n|-- ..<br> \nESR X<br> \n|-- project 1<br> \n  |-- data<br> \n    |-- ..<br> \n  |-- Arguments.py<br> \n  |-- config.yaml<br> \n  |-- main.py<br>\n  |-- datamodule.py<br>\n  |-- pl_framework.py<br>\n\n## Contributors\n\nAll fellows of the AIDD consortium have contributed to the packaged.\n\n## Code of Conduct\n\nEveryone interacting in the codebase, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).\n\n \n',
    'author': 'Peter Hartog',
    'author_email': 'peter.hartog@hotmail.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidd-msca/aidd-codebase',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
