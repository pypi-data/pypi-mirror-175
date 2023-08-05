# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beersmith_direct']

package_data = \
{'': ['*']}

install_requires = \
['aracnid-config>=1.0,<2.0',
 'aracnid-logger>=1.0,<2.0',
 'aracnid-utils>=1.0,<2.0',
 'beautifulsoup4>=4.0,<5.0',
 'hjson>=3.0,<4.0',
 'i-mongodb>=2.0,<3.0',
 'xmltodict>=0.12,<0.13']

setup_kwargs = {
    'name': 'beersmith-direct',
    'version': '1.3.0',
    'description': 'Custom interface to Beersmith database',
    'long_description': '# Beersmith Direct\n\nWe use Beersmith to design our beer recipes. The application interface is nice for a user, but there is no API for direct access. This package reads the recipe files and saves them into a MongoDB database.\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your local machine for development and testing purposes.\n\n### Prerequisites\n\nThis package supports the following version of Python. It probably supports older versions, but they have not been tested.\n\n- Python 3.10 or later\n\n### Installing\n\nInstall the latest package using pip.\n\n```bash\n$ pip install beersmith-direct\n```\n\nEnd with an example of getting some data out of the system or using it for a little demo\n\n## Running the tests\n\nExplain how to run the automated tests for this system\n\n```bash\n$ python -m pytest\n```\n\n## Usage\n\nTODO\n\n## Authors\n\n- **Jason Romano** - [Aracnid](https://github.com/aracnid)\n\nSee also the list of [contributors](https://github.com/lakeannebrewhouse/beersmith-direct/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Jason Romano',
    'author_email': 'aracnid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lakeannebrewhouse/beersmith-direct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
