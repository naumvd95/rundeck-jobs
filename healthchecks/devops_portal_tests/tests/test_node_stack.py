import logging

import pytest

from devops_portal_tests.models.stack_manager import StackManager


logger = logging.getLogger(__name__)


@pytest.mark.healthcheck
@pytest.mark.node_stack_healthcheck
def test_stack_availability(env_config):
    stack_manager = StackManager(env_config.get('nodes', {}))
    for node in stack_manager.nodes:
        logger.debug('Checking the node {!r}'.format(node.hostname))
        node.ssh_client.exec_command('uptime')
