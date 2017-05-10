#!/bin/bash
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev libyaml-dev python-dev python-pip

sudo pip install virtualenv
sudo virtualenv venv-devops-portal-test
ls -al
cd /var/rundeck/projects/cicd/scm/healthchecks
source venv-devops-portal-test/bin/activate
pip install -r requirements.txt
pip install -r test-requirements.txt
export CONFIG_FILE_PATH=$RD_OPTION_CONFIG_PATH
pytest -m $RD_OPTION_HEALTHCHECK
