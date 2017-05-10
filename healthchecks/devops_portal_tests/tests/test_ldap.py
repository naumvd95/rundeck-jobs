import logging

import pytest
from devops_portal_tests.helpers.utils import load_config

import os
import ldap
import ldap.modlist as modlist

logger = logging.getLogger(__name__)
ldap_config = load_config()['services']['ldap']
ldap_url = ldap_config['endpoint']
ldap_admin = ldap_config['credentials']['username']
ldap_password = ldap_config['credentials']['password']
dn = os.getenv('LDAP_DN') or 'cn=ldap_test,ou=people,dc=cicd-lab-dev,dc=local'
base_dn = ldap_config['credentials']['base_dn']


@pytest.fixture(scope="module", autouse=True)
def ldap_connect():
    client = ldap.initialize(ldap_url)
    return client


def authenticate(client, ldap_login, ldap_pass):
    assert client.simple_bind_s(ldap_login, ldap_pass)
    logger.debug("user authenticated successfully")


def exist_user(client, base_dn, search_f):
    search_scope = ldap.SCOPE_SUBTREE
    ldap_result_id = client.search(base_dn, search_scope, search_f)
    result_set = []
    while True:
        result_type, result_data = client.result(ldap_result_id, 0)
        if (result_data == []):
            break
        else:
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
    if (result_set == []):
        return False
    else:
        logger.debug('test-user already exists, it will be re-created')
        logger.debug(result_set)
        return True


def create_user(client, dn, attributes=None):
    # Create new user for healthcheck
    attrs = {
        'objectclass': [
            'top',
            'shadowAccount',
            'inetOrgPerson',
            'posixAccount',
        ],
        'cn': 'ldap_test',
        'userPassword': 'ldap_test',
        'loginShell': '/bin/bash',
        'uidNumber': '20002',
        'gidNumber': '20001',
        'gecos': 'Administrator',
        'sn': 'Root',
        'homeDirectory': '/home/ldap_test',
        'mail': 'portal@gmail.com',
        'givenName': 'ldap_test',
        'uid': 'admin',
    }

    if attributes:
        attrs.update(attributes)
    # Convert our dict to nice syntax for the add-function using modlist-module
    ldif = modlist.addModlist(attrs)
    assert client.add_s(dn, ldif)
    logger.debug("user created successfully")


def delete_user(client, dn):
    assert client.delete_s(dn)
    logger.debug("user removed successfully")


def ldap_disconnect(client):
    client.unbind_s()


@pytest.mark.healthcheck
@pytest.mark.ldap_healthcheck
@pytest.mark.ldap_server_healthcheck
def test_ldap_new_user(ldap_connect):
    client = ldap_connect
    authenticate(client, ldap_admin, ldap_password)
    if exist_user(client, base_dn, 'cn=*ldap_test*'):
        delete_user(client, dn)
    create_user(client, dn)
    logger.info("try to authenticate with new user")
    authenticate(client, dn, "ldap_test")
    # teardown
    logger.info("remove created user, using admin-dn")
    authenticate(client, ldap_admin, ldap_password)
    delete_user(client, dn)
    ldap_disconnect(client)
