# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['combined_energy', 'tests']

package_data = \
{'': ['*'], 'tests': ['fixtures/api-responses/*']}

install_requires = \
['aiohttp', 'pydantic']

setup_kwargs = {
    'name': 'combined-energy-api',
    'version': '0.5',
    'description': 'Python interface to the Combined Energy API',
    'long_description': '# Python: Asynchronous client for Combined Energy API\n\nProvides an async Python 3.8+ interface for the http://combined.energy/ monitoring platform API.\n\n> Note this API client is reverse engineered from observing requests being made  \n> in the web-application. Please report any failures to read data, this is likely\n> to occur for readings as I am only able to create entries for devices that I \n> have.\n\n## Installation\n\nInstall from PyPI\n\n```shell\npython3 -m pip install combined-energy-api\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom combined_energy import CombinedEnergy\nfrom combined_energy.helpers import ReadingsIterator\n\nasync def main():\n    """\n    Example using Combined Energy API client.\n    """\n\n    async with CombinedEnergy(\n        mobile_or_email="user@example.com",\n        password="YOUR_COMBINED_ENERGY_PASSWORD",\n        installation_id=9999,\n    ) as combined_energy:\n\n        status = await combined_energy.communication_status()\n        print(status)\n\n        # To generate a stream of readings use the iterator, this example fetches\n        # data in 5 minute increments\n        async for readings in ReadingsIterator(combined_energy, increment=300):\n            print(readings)\n            await asyncio.sleep(300)\n\nasyncio.run(main())\n\n```\n\n\n### Development Environment\n\nYou will need:\n\n- Python 3.8+\n- poetry\n- pre-commit\n\nEnsure pre-commit is installed into your git repository with `pre-commit install`. \n',
    'author': 'Tim Savage',
    'author_email': 'tim@savage.company',
    'maintainer': 'Tim Savage',
    'maintainer_email': 'tim@savage.company',
    'url': 'https://github.com/timsavage/combined-energy-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
