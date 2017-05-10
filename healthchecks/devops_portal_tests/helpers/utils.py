import logging
import json

from devops_portal_tests.settings import CONFIG_FILE_PATH
from devops_portal_tests.clients.rest_client import SimpleRESTClient


logger = logging.getLogger(__name__)


def load_config():
    with open(CONFIG_FILE_PATH) as config_file:
        config = json.load(config_file)
    return config


def init_restclient(service_name, config):
    service_data = config['services'].get(service_name, None)
    if service_name is None:
        raise Exception('Data for service {!r} is not provided. '
                        'Check config: \n {}'.format(service_name, config))
    if service_data.get('credentials', False):
        client = SimpleRESTClient(
            service_data['endpoint'],
            username=service_data['credentials'].get('username', None),
            password=service_data['credentials'].get('password', None),
            token=service_data['credentials'].get('token', None))
    else:
        client = SimpleRESTClient(service_data['endpoint'])
    logger.debug('{} client is defined'.format(service_data))
    return client
