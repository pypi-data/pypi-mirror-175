# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sinfonia_tier3', 'tests']

package_data = \
{'': ['*'], 'sinfonia_tier3': ['openapi/*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'importlib-resources>=5.0,<6.0',
 'openapi-core>=0.14.2,<0.15.0',
 'pyyaml>=6.0,<7.0',
 'randomname>=0.1.5,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'wgconfig>=0.2.2,<0.3.0',
 'xdg>=5.1.1,<6.0.0',
 'yarl>=1.7.2,<2.0.0',
 'zeroconf>=0.39.4,<0.40.0']

entry_points = \
{'console_scripts': ['sinfonia-tier3 = sinfonia_tier3.cli:main']}

setup_kwargs = {
    'name': 'sinfonia-tier3',
    'version': '0.3.0',
    'description': 'Tier 3 component of the Sinfonia system',
    'long_description': 'None',
    'author': 'Carnegie Mellon University',
    'author_email': 'satya+group@cs.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
