Tests for the check of Devops Portal

Prerequisites:
==============

Code requirements:
------------------
Install requirements with 'pip install -r requirements.txt'

Prepared environment:
---------------------

For the proper test execution you need to define environment config in json file, like that::

    {
      "services": {
        "haproxy":{
        "endpoint": "http://172.16.10.254:9600/"
        },
        "elasticsearch": {
          "endpoint": "http://172.16.10.254:9200/"
        },
        "gerrit": {
          "endpoint": "http://172.16.10.254:8080/"
        },
        "jenkins": {
          "endpoint": "http://172.16.10.254:8081/"
        },
        "pushkin": {
          "endpoint": "http://172.16.10.254:8887/"
        },
        "rundeck": {
          "endpoint": "http://172.16.10.254:4440/",
          "credentials": {
              "token": "password",
              "username": "admin",
              "password": "password"
            }
        },
        "ldap": {
          "endpoint": "ldap://172.16.10.254:389/",
          "credentials": {
              "username": "cn=admin,dc=cicd-lab-dev,dc=local",
              "password": "password",
              "base_dn": "ou=people,dc=cicd-lab-dev,dc=local"
            }
        }
        },
      "nodes":{
        "ci01":{
          "ip": "172.16.10.11",
          "username": "root",
          "pkey": "private_key"
          },
        "ci02":{
          "ip": "172.16.10.12",
          "username": "root",
          "pkey": "private_key"
        },
        "ci03":{
          "ip": "172.16.10.13",
          "username": "root",
          "pkey": "private_key"
        }
      }
    }

.. code:: bash

    export CONFIG_FILE_PATH=/path/to/environment/config.json

Build and install as python package
===================================
Build dist with next command:
   python setup.py sdist

or:
   tox -e build

Run install on target machine:
   pip install devops_portal_tests-1.0.tar.gz --process-dependency-links

where "--process-dependency-links" flag is necessary.


Installing dependencies and system packages
===========================================
To install system packages run:
   apt install -y build-essential libssl-dev libffi-dev python-dev libyaml-dev python-dev python-pip

Create and activate virtualenv:
   pip install virtualenv
   virtualenv venv-devops-portal-test
   source venv-devops-portal-test/bin/activate

Install dependencies, if you aren't using this project as package:
   pip install -r requirements.txt

Run tests
=========
So, on this step you have described environment and you are ready to run tests.
For this you need to execute the command above, if you have installed devops_portal_tests from a package:

.. code:: bash

    devops-portal-tests check --type healthcheck --xml_path result.xml

or, if you have source code from repo (execute from the project root directory):

.. code:: bash

    pytest -m healthcheck

or:

.. code:: bash

    python devops_portal_tests/cli.py check --type healthcheck --xml_path result.xml

Anyway, you should get result of testing in stdout and saved result xml file.
