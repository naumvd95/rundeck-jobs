import logging

import pytest

from devops_portal_tests.helpers.utils import init_restclient

logger = logging.getLogger(__name__)


def parse_haproxy_status(status):
    status = status.split('\n')[1:-1]
    status = [service.split(',') for service in status]
    services_status = {}
    for service_status in status:
        if service_status[0] in services_status:
            services_status[service_status[0]].append(
                {'node': service_status[1],
                 'status': service_status[17]}
            )
        else:
            services_status[service_status[0]] = []
    return services_status


@pytest.mark.healthcheck
@pytest.mark.haproxy_healthcheck
def test_haproxy_backends(env_config):
    # init rest client
    haproxy_client = init_restclient('haproxy', env_config)
    response = haproxy_client.get(endpoint='/haproxy?stats;csv')
    assert response.status_code == 200

    status = response.text
    logger.debug('The state of haproxy backends: \n {}'
                 .format(status))
    services_status = parse_haproxy_status(status)
    logger.debug('The state of haproxy backends (pretty view): \n {}'
                 .format(services_status))
    failed_services = dict(
        [(failed_service, data)
         for failed_service, data in services_status.items()
         for endpoint in data
         if endpoint['status'] not in ['UP', 'OPEN']]
    )
    assert not failed_services,\
        'There are failed services:\n {}'.format(failed_services)
