ssh.py
======

A very small and smart SSH configuration tool.


Quick start
------------

Install from pip or run from source code

.. code-block:: bash

  $ pip install ssh.py

Or

.. code-block:: bash

  $ pip install -r requirements.txt
  $ python ssh.py -h


Get all SSH key in local host

.. code-block:: bash

  $ python ssh.py list key
  +-----------------------+
  | Private Key Name      |
  +-----------------------+
  | aws.pem               |
  | github_rsa            |
  | gitlab.com_rsa        |
  | gitlab_rsa            |
  | tmp                   |
  | tmp1                  |
  +-----------------------+

Get all SSH host config information

.. code-block:: bash

  (ssh.py)➜  ssh.py git:(master) ✗ python ssh.py list host
  +-------------------------+----------------------------------------------------+-------------+----------------------------------+
  | host                    | hostname                                           | user        | identityfile                     |
  +-------------------------+----------------------------------------------------+-------------+----------------------------------+
  | ['test1112.me']         | ec2-xx-xxx-xxx-139.us-xxxx-2.compute.amazonaws.com | xxx-user    | ['~/.ssh/dddddddd-aws.pem']      |
  | ['github.com']          | ['github.com']                                     | xxxxxxxxxxx | ['~/.ssh/github_rsa']            |
  | ['gitlab.com']          | ['gitlab.com']                                     | xxxxxxxx    | ['~/.ssh/gitlab.com_rsa']        |
  +-------------------------+----------------------------------------------------+-------------+----------------------------------+
