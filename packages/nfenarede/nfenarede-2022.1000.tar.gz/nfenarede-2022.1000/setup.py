# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'system'}

packages = \
['system',
 'system.cdk',
 'system.integracao.bling',
 'system.integracao.bling.src',
 'system.microservices.cobranca_clientes',
 'system.nfenarede_api',
 'system.nfenarede_api.api',
 'system.nfenarede_api.api.emitente',
 'system.nfenarede_core.python',
 'system.nfenarede_core.python.api',
 'system.nfenarede_core.python.api.emitente',
 'system.nfenarede_core.python.libs',
 'system.nfenarede_core.python.utils']

package_data = \
{'': ['*'], 'system': ['infra/*', 'nfenarede_core/*']}

install_requires = \
['Unidecode>=1.3.6,<2.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'amazon-dax-client>=2.0.1,<3.0.0',
 'aws-cdk-lib>=2.40.0,<3.0.0',
 'aws-cdk.aws-apigatewayv2-integrations-alpha>=2.45.0-alpha.0,<3.0.0',
 'aws-cdk.aws-lambda-python-alpha>=2.45.0-alpha.0,<3.0.0',
 'aws-lambda-powertools>=2.1.0,<3.0.0',
 'click>=8.0.1',
 'email-validator>=1.2.1,<2.0.0',
 'fastapi>=0.85.0,<0.86.0',
 'mangum>=0.15.1,<0.16.0',
 'mysql-connector-python>=8.0.30,<9.0.0',
 'mysqlclient>=2.1.1,<3.0.0',
 'pydantic>=1.9.1',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'simplejson>=3.17.6,<4.0.0']

entry_points = \
{'console_scripts': ['nfenarede = nfenarede.__main__:main']}

setup_kwargs = {
    'name': 'nfenarede',
    'version': '2022.1000',
    'description': 'NFe na rede',
    'long_description': "# NFe na rede\n\n[![PyPI](https://img.shields.io/pypi/v/nfenarede.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/nfenarede.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/nfenarede)][python version]\n[![License](https://img.shields.io/pypi/l/nfenarede)][license]\n\n[![Read the documentation at https://nfenarede.readthedocs.io/](https://img.shields.io/readthedocs/nfenarede/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/bnsouza/nfenarede/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/bnsouza/nfenarede/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/nfenarede/\n[status]: https://pypi.org/project/nfenarede/\n[python version]: https://pypi.org/project/nfenarede\n[read the docs]: https://nfenarede.readthedocs.io/\n[tests]: https://github.com/bnsouza/nfenarede/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/bnsouza/nfenarede\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Version\n\n2022.1000\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _NFe na rede_ via [pip] from [PyPI]:\n\n```console\n$ pip install nfenarede\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_NFe na rede_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/bnsouza/nfenarede/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/bnsouza/nfenarede/blob/main/LICENSE\n[contributor guide]: https://github.com/bnsouza/nfenarede/blob/main/CONTRIBUTING.md\n[command-line reference]: https://nfenarede.readthedocs.io/en/latest/usage.html\n",
    'author': 'Bruno Souza',
    'author_email': 'bruno@komu.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bnsouza/nfenarede',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
