===============
**aws-cfstack**
===============

Overview
--------

Get AWS CloudFormation stack template and parameters.

Prerequisites
-------------

- *Python >= 3.6*
- *aws-authenticator (https://pypi.org/project/aws-authenticator/) >= 2022.10.1.0*

Required Arguments
------------------

- Output path (to store module artifacts)
- AWS authentication method (profile, iam, or sso)

Conditional Arguments
---------------------

If authenticating with named profiles:

- AWSCLI profile name

If authenticating with IAM acccess key credentials:

- AWS access key id
- AWS secret access key

If authenticating with SSO:

- AWS account ID
- AWS SSO Permission Set (role) name
- AWS SSO login URL

Usage
-----

Installation:

.. code-block:: BASH

   pip3 install aws-cfstack
   # or
   python3 -m pip install aws-cfstack

In Python3 authenticating with named profiles:

.. code-block:: PYTHON

   import aws_cfstack

   aws_cfstack.get_stack(
      '/home/username/Desktop',
      'profile',
      profile_name='<profile_name>'
   )

In BASH authenticating with named profiles:

.. code-block:: BASH

   python [/path/to/]aws_cfstack \
   -o <output_path> \
   -m profile \
   -p <profile_name>
