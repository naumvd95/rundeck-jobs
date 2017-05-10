import logging

import pytest

from devops_portal_tests.helpers.utils import load_config
from devops_portal_tests.models.ssh_manager import SSHManager


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def env_config():
    return load_config()


@pytest.fixture(scope="session")
def close_ssh_connections():
    ssh_manager = SSHManager()
    yield ssh_manager
    del ssh_manager
