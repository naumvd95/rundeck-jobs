import logging

import pytest

from datetime import datetime

from devops_portal_tests.helpers.utils import init_restclient

logger = logging.getLogger(__name__)


@pytest.mark.healthcheck
@pytest.mark.elasticsearch_healthcheck
@pytest.mark.elasticsearch_cluster_healthcheck
def test_elasticsearch_cluster(env_config):
    # init rest client
    elastic_client = init_restclient('elasticsearch', env_config)
    response = elastic_client.get(endpoint='/_cluster/health')
    data = response.json()
    logger.debug(data)
    assert (data['status'] != 'red'), 'Detailed description:\n{}'.format(data)


@pytest.mark.healthcheck
@pytest.mark.elasticsearch_healthcheck
@pytest.mark.elasticsearch_data_healthcheck
def test_elasticsearch_data(env_config):
    # init rest client
    elastic_client = init_restclient('elasticsearch', env_config)
    resp = elastic_client.post(
        endpoint="/notifications/notification?pretty&pretty",
        json={
            'title': 'cicd',
            'content': 'Elasticsearch: data-healthcheck',
            'timestamp': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")
        }
    )
    logger.debug(resp.json())
    assert (resp.status_code == 201), \
        'Detailed description:\n {} '.format(resp.json())
