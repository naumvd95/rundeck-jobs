import logging

from devops_portal_tests.models.ssh_manager import SSHManager


logger = logging.getLogger(__name__)
ssh_manager = SSHManager()


class Node(object):

    def __init__(self, hostname, ip, creds=None):
        self.hostname = hostname
        self.ip = ip
        self.creds = creds
        self.__ssh_client = None
        self.__status = None

    @property
    def ssh_client(self):
        if self.__ssh_client is None:
            self.__ssh_client = ssh_manager.create_connection(
                self.ip, self.creds.get('username'),
                password=self.creds.get('password', None),
                pkey=self.creds.get('pkey', None))
        return self.__ssh_client

    @property
    def status(self):
        if self.__status is None:
            # TODO
            pass
        return self.__ssh_client


class StackManager(object):

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.nodes = []

        for hostname, data in self.config.items():
            creds = {
                'username': data.get('username'),
                'password': data.get('password'),
                'pkey': data.get('pkey')
            }
            self.nodes.append(Node(hostname, data['ip'], creds))

    def add_node(self, node_data):
        for hostname, data in node_data.items():
            logger.debug('Node {} will be add into stack manager pool'
                         .format(hostname))

            creds = {
                'username': data.get('username'),
                'password': data.get('password'),
                'pkey': data.get('pkey')
            }
            self.nodes.append(Node(hostname, data['ip'], creds))

    def del_node(self, hostname):
        logger.debug('Node {} will be deleted from stack manager pool'
                     .format(hostname))
        # TODO: process the case when filter returns an empty list
        node = filter(lambda x: x.hostname == hostname, self.nodes)[0]
        node.ssh_client.ssh.close()
        self.nodes.remove(node)

    def get_node_by_status(self, status):
        return filter(lambda x: x.status == status, self.nodes)
