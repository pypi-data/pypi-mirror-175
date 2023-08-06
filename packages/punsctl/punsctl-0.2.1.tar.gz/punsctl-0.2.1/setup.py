# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['punsctl']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['punsctl = punsctl.main:main']}

setup_kwargs = {
    'name': 'punsctl',
    'version': '0.2.1',
    'description': "POSIX User's Namespace Control",
    'long_description': '### `The project is currently under development and is not ready for use in production.`\n\n# punsctl - POSIX User\'s Namespace Control\n\n[![PyPI Version](https://img.shields.io/pypi/v/punsctl)](https://pypi.python.org/pypi/punsctl)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/punsctl?style=flat-square)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/punsctl)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/punsctl)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/punsctl)\n\n[![codecov](https://codecov.io/github/alekbuza/punsctl/branch/main/graph/badge.svg?token=OMHOSME5ZB)](https://codecov.io/github/alekbuza/punsctl)\n[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)\n\n\nThe `punsctl` utility manages multiple namespaces (user environments) for the current POSIX user.\nThat means the user can have multiple "_profiles_" for the same or different tool configurations in the same user account\n(`~/.ssh`, `~/.gitconfig`, `~/.gnupg`, `~/.config`, `~/.config/nvim`, ...).\nThe user can create, delete, activate and deactivate namespaces without additional permissions.\n\n## Installation\n\n```sh\npip install punsctl\n```\n\n## Usage\n\n```txt\npunsctl <options>\n\noptions:\n    -h                  Help menu\n    -r                  Root path                 (Default: ~/.ns)\n    -s                  Symlink path              (Default: ~/)\n    -l                  List namespaces\n    -n <namespace>      Create namespace\n    -x <namespace>      Delete namespace\n    -a <namespace>      Activate namespace\n    -d                  Deactivate namespaces\n```\n\n### List all namespaces\n```sh\npunsctl -l\n```\n\n### List all namespaces from the `non-default` root path\n```sh\npunsctl -p <root_path> -l\n```\n\n### Create new namespace\n```sh\npunsctl -n <namespace>\n```\n\n### Create a new namespace in the `non-default` root path\n```sh\npunsctl -p <root_path> -n <namespace>\n```\n\n### Delete namespace\n```sh\npunsctl -x <namespace>\n```\n\n### Delete namespace in `non-default` root path\n```sh\npunsctl -p <root_path> -x <namespace>\n```\n\n### Activate namespace\n```sh\npunsctl -a <namespace>\n```\n\n### Activate the namespace from the `non-default` root path\n```sh\npunsctl -p <root_path> -a <namespace>\n```\n\n### Activate the namespace from the `non-default` root path and change the symlink path\n\n```sh\npunsctl -p <root_path> -s <symlink_path> -a <namespace>\n```\n\n### Deactivate namespaces\n```sh\npunsctl -d\n```\n\n',
    'author': 'Aleksandar Buza',
    'author_email': 'me@aleksandarbuza.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alekbuza/punsctl',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
