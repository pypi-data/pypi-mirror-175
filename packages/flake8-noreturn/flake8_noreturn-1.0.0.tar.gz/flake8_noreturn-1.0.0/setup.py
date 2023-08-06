# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_noreturn']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=5.0.4,<6.0.0']

setup_kwargs = {
    'name': 'flake8-noreturn',
    'version': '1.0.0',
    'description': 'A flake8 plugin to detect return None (-> None) type hints.',
    'long_description': '# flake8-noreturn\n![](https://img.shields.io/pypi/v/flake8-noreturn.svg)\n![](https://img.shields.io/pypi/pyversions/flake8-noreturn.svg)\n![](https://img.shields.io/pypi/l/flake8-noreturn.svg)\n![](https://img.shields.io/pypi/dm/flake8-noreturn.svg)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/izikeros/flake8-noreturn/main.svg)](https://results.pre-commit.ci/latest/github/izikeros/trend_classifier/main)\n[![Maintainability](https://api.codeclimate.com/v1/badges/081a20bb8a5201cd8faf/maintainability)](https://codeclimate.com/github/izikeros/flake8-noreturn/maintainability)\n\nFlake8 plugin to check for using `-> None:` type hint for return type. Helps to replace them with `-> NoRetun` type hint from typing.\n\n**Why to use `NoReturn` type hint?**\n\nUsing `NoReturn` type hint:\n- is more explicit and helps to avoid confusion with `None` value,\n- helps to avoid bugs when using `None` as a default value for function arguments.\n- helps mypy to detect unreachable code\n-\n## Installation\nUse pip to install the package:\n```sh\n$ pip3 install flake8-noreturn\n```\n\n## Usage\n\n```sh\n$ flake8 .\n```\n\nto select only `flake8-noreturn` errors:\n\n```sh\n$ flake8 --select NR .\n```\n\n## Rules\nCurrently, the plugin checks implements only one rule:\n\n`NR001 Using -> None.`\nIndicates usage of `-> None:` type hint for return type.\n\nExamples:\n```python\ndef foo() -> None:\n    pass\n```\nwill raise NR001.\n\n```python\nfrom typing import NoReturn\n\ndef foo() -> NoReturn:\n    pass\n```\nwill not raise NR001.\n\n```python\ndef foo() -> tuple[int, None]:\n    return 2, None\n```\nwill not raise NR001.\n\n## Related Projects\n\nThere is a [flake8-no-types](https://github.com/adamchainz/flake8-no-types) which was a heavy inspiration for this project.\n\n## Credits\n\nThank you [adamchainz](https://github.com/adamchainz) for the inspiring [article](https://adamj.eu/tech/2021/05/20/python-type-hints-whats-the-point-of-noreturn/) and the [flake8-no-types](https://github.com/adamchainz/flake8-no-types) which helped me to create this plugin.\n\n## License\n\n[MIT](https://izikeros.mit-license.org/) © [Krystian Safjan](https://safjan.com).\n',
    'author': 'Krystian Safjan',
    'author_email': 'ksafjan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
