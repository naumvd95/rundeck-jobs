import requests
from requests.compat import urljoin


class SimpleRESTClient(object):

    def __init__(self, url, username=None, password=None, token=None):
        self.url = url
        self.username = username
        self.password = password
        self.token = token
        self.http = requests.Session()

    def make_url(self, endpoint=None):
        return urljoin(self.url, endpoint) if endpoint else self.url

    def get(self, endpoint=None, **kwargs):
        return self.http.get(self.make_url(endpoint=endpoint), **kwargs)

    def post(self, endpoint=None, data=None, json=None, **kwargs):
        return self.http.post(self.make_url(endpoint=endpoint), data=data,
                              json=json, **kwargs)

    def delete(self, endpoint=None, **kwargs):
        return self.http.delete(self.make_url(endpoint=endpoint), **kwargs)
