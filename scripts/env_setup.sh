#!/bin/bash
apt-get install -y build-essential libssl-dev libffi-dev python-dev libyaml-dev python-dev python-pip

pip install virtualenv
virtualenv venv-devops-portal-test
source venv-devops-portal-test/bin/activate
pip install -r requirements.txt
pip install -r test-requirements.txt

pytest -m $HEALTHCHECK
