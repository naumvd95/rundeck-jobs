import logging

import six

from devops_portal_tests.clients.ssh_client import SSHClient


logger = logging.getLogger(__name__)


class SingletonMetaClass(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class SSHManager(six.with_metaclass(SingletonMetaClass, object)):
    """Manager SSH connections"""

    def __init__(self):
        self.connections = {}

    def __del__(self):
        for client in self.connections.values():
            del client

    def create_connection(self, host, username, password=None, pkey=None,
                          port=22, timeout=300, channel_timeout=10):
        if (host, port) not in self.connections:
            self.connections[(host, port)] = SSHClient(
                host, username, password=password, pkey=pkey,
                port=port, timeout=timeout, channel_timeout=channel_timeout)
        logger.debug('The current connections: {}'.format(self.connections))
        return self.connections[(host, port)]
