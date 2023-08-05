# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_cfstack']

package_data = \
{'': ['*']}

install_requires = \
['aws-authenticator>=2022.10.1.0,<2023.0.0.0']

setup_kwargs = {
    'name': 'aws-cfstack',
    'version': '2022.11.1.1',
    'description': 'Get AWS CloudFormation stack template and parameters.',
    'long_description': '===============\n**aws-cfstack**\n===============\n\nOverview\n--------\n\nGet AWS CloudFormation stack template and parameters.\n\nPrerequisites\n-------------\n\n- *Python >= 3.6*\n- *aws-authenticator (https://pypi.org/project/aws-authenticator/) >= 2022.10.1.0*\n\nRequired Arguments\n------------------\n\n- Output path (to store module artifacts)\n- AWS authentication method (profile, iam, or sso)\n\nConditional Arguments\n---------------------\n\nIf authenticating with named profiles:\n\n- AWSCLI profile name\n\nIf authenticating with IAM acccess key credentials:\n\n- AWS access key id\n- AWS secret access key\n\nIf authenticating with SSO:\n\n- AWS account ID\n- AWS SSO Permission Set (role) name\n- AWS SSO login URL\n\nUsage\n-----\n\nInstallation:\n\n.. code-block:: BASH\n\n   pip3 install aws-cfstack\n   # or\n   python3 -m pip install aws-cfstack\n\nIn Python3 authenticating with named profiles:\n\n.. code-block:: PYTHON\n\n   import aws_cfstack\n\n   aws_cfstack.get_stack(\n      \'/home/username/Desktop\',\n      \'profile\',\n      profile_name=\'<profile_name>\'\n   )\n\nIn BASH authenticating with named profiles:\n\n.. code-block:: BASH\n\n   python [/path/to/]aws_cfstack \\\n   -o <output_path> \\\n   -m profile \\\n   -p <profile_name>\n\nCaveat\n------\n\n- This module creates files within the specified *output_path*.\n- All stack instances whose names start with "**StackSet-**" are filtered out. This module was not intended to work with stack sets, although it can easily be expanded to do so.\n- DOS line-endings ("**\\r**") are removed from the outputs. Only Unix line-endings ("**\\n**") are retained.\n',
    'author': 'Ahmad Ferdaus Abd Razak',
    'author_email': 'ahmad.ferdaus.abd.razak@ni.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fer1035/pypi-aws_cfstack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
