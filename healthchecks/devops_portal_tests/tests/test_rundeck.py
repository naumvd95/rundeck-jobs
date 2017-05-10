import logging

import pytest

from devops_portal_tests.helpers.utils import init_restclient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="class", autouse=True)
def rundeck(env_config):
    client = init_restclient('rundeck', env_config)
    authenticate(client)
    return client


def authenticate(client):
    resp = client.post(
        endpoint='/j_security_check',
        data={
            'j_username': client.username,
            'j_password': client.password
        }
    )
    client.http.params.update({'format': 'json'})
    if (resp.status_code != 200 or
            '/user/error' in resp.url or
            '/user/login' in resp.url):
        raise Exception('The authorization failed')
    logger.debug('Session authorized in Rundeck')


def get_project(client, name):
    resp = client.get(
        endpoint="/api/18/project/{}".format(name))
    status_code = resp.status_code
    if status_code == 200:
        return resp.json()
    elif status_code == 404:
        return None


def create_project(client, name):
    config = create_project_config(name)
    logger.debug("create_project: %s", name)
    logger.warning("create_project.config: %s/%s", name, config)
    kwargs = {'allow_redirects': False}
    resp = client.post(
        endpoint="/api/18/projects",
        json={
            'name': name,
            'config': config,
        },
        **kwargs
    )
    if resp.status_code == 201:
        return resp.json()
    logger.debug("create_project: %s", name)


def delete_project(client, name):
    resp = client.delete(
        endpoint="/api/18/project/{}".format(name))
    status_code = resp.status_code
    if status_code != 204:
        logger.error('Project was not removed')


def create_project_config(name, config=None):
    config = dict(config) if config else {}
    config.update({
        'resources.source.1.config.file':
        "/var/rundeck/projects/{}/etc/resources.yaml".format(name),
        'resources.source.1.config.format': 'resourceyaml',
        'resources.source.1.config.generateFileAutomatically': 'true',
        'resources.source.1.config.includeServerNode': 'false',
        'resources.source.1.config.requireFileExists': 'false',
        'project.ssh-keypath': '/var/rundeck/.ssh/id_rsa',
        'resources.source.1.type': 'file',
    })
    return config


@pytest.mark.healthcheck
@pytest.mark.rundeck_healthcheck
def test_rundeck_availability(rundeck):
    resp = rundeck.get(endpoint="/metrics/healthcheck")
    assert resp.status_code == 200
    rundeck_health = resp.json()['quartz.scheduler.threadPool']['healthy']
    logger.debug('Rundeck service is alive - {}'.format(rundeck_health))
    assert rundeck_health is True
