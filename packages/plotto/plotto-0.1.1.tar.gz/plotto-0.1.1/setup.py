# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotto', 'plotto.datasets', 'plotto.marks', 'plotto.tests']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2.0,<5.0.0', 'numpy>=1.23.4,<2.0.0', 'pandas>=1.4,<1.5']

setup_kwargs = {
    'name': 'plotto',
    'version': '0.1.1',
    'description': 'functions to create interactive charts with Altair',
    'long_description': 'plotto contains a function to display a set of interactive charts created with Altair\n\n## Installing\n\nThe latest release can be installed using pip\n\n```bash\npip install plotto\n```\n\nsee the [Documentation](https://plotto.readthedocs.io/en/latest/) for more details.\n',
    'author': 'Bernardo Dionisi',
    'author_email': 'bernardo.dionisi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bernardodionisi/plotto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
