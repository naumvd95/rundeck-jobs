import logging

import pytest
import docker

logger = logging.getLogger(__name__)


@pytest.mark.healthcheck
@pytest.mark.swarm_healthcheck
@pytest.mark.nodes_state_healthcheck
def test_nodes_state():
    """All nodes should be in active state"""
    client = docker.from_env()
    fail_list = []
    for node in client.nodes():
        node_name = node['Description']['Hostname']
        status = node['Spec']['Availability']
        logger.debug('The node {!r} has status {!r}'.format(node_name, status))
        if status != 'active':
            fail_list.append(str(node_name + ' state=' + status))
    assert (len(fail_list) == 0), 'There are failed nodes'.format(fail_list)


@pytest.mark.healthcheck
@pytest.mark.swarm_healthcheck
@pytest.mark.service_replicas_healthcheck
def test_service_replicas():
    """All services should be replicated"""
    client = docker.from_env()
    fail_list = []
    for service in client.services():
        service_name = service['Spec']['Name']
        r = service['Spec']['Mode']['Replicated']['Replicas']
        logger.debug('Service {!r} has {!r} replicas'.format(service_name, r))
        if r == 0:
            fail_list.append(str(service_name + ' replicas=' + r))
    assert (len(fail_list) == 0), 'There are failed services'.format(fail_list)
