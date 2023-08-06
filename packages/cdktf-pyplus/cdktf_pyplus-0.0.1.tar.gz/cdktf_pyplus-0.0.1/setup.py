# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdktf_pyplus', 'cdktf_pyplus.aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.0,<2.0.0',
 'cdktf-cdktf-provider-aws>=10.0.2,<11.0.0',
 'cdktf-cdktf-provider-random>=3.0.11,<4.0.0',
 'cdktf>=0.13.2,<0.14.0',
 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'cdktf-pyplus',
    'version': '0.0.1',
    'description': 'A python lib to help build cdktf project',
    'long_description': '# Simple but Powerful python lib for terraform cdk\n',
    'author': 'jingwei zhu',
    'author_email': 'jingwei.zhu@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
