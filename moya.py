import json
from requests import Session
from enum import Enum
from functools import partial

class Session(Session):
    """extending Session to work with pickling"""
    def __getstate__(self):
        attrs = ['headers', 'cookies', 'auth', 'timeout', 'proxies', 'hooks', \
            'params', 'config', 'verify']
        return {attr: getattr(self, attr) for attr in attrs}

    def __setstate__(self, state):
        for name, value in state.items():
            setattr(self, name, value)
        self.poolmanager = PoolManager(num_pools=self.config.get('pool_connections'),
                                       maxsize=self.config.get('pool_maxsize'))

class HTTPMethod(Enum):
    get = 1
    post_json = 2
    post_form = 3

class Endpoint(Enum):
    """abstract class, subclassers must at least implement the method()
    property method"""

    @property
    def url(self):
        """returns the url for the endpoint, default is just Endpoint.value"""
        return self.value

    @property
    def method(self):
        """returns the HTTPMethod associated with the endpoint"""
        raise NotImplementedError("class {} doesn't implement method()"\
                                  .format(self.__class__.__name__))

    @property
    def parameters(self):
        """returns the parameters string for the request, default is None"""
        return None

    @property
    def headers(self):
        """returns any custom headers for the request, default is None"""
        return None

class Provider:
    def __init__(self):
        self.session = Session()

    def request(self,
                endpoint,
                loud=False,
                mitmproxied=False):
        """make a request to the provided endpoint, either using the session
        object provided or creating and returning a new one"""
        url = endpoint.url
        method = endpoint.method
        parameters = endpoint.parameters
        headers = endpoint.headers

        # debug printing
        if loud:
            print("{} request at {} ...".format(method.name, url))
            if parameters:
                print("parameters: {}".format(json.dumps(parameters)))

        proxies = {
            'http': 'http://localhost:8081',
            'https': 'http://localhost:8081'
        } if mitmproxied else None

        return {
            HTTPMethod.get: \
            partial(self.session.get, params=parameters),
            HTTPMethod.post_json: \
            partial(self.session.post, json=parameters),
            HTTPMethod.post_form: \
            partial(self.session.post, data=parameters)
        }.get(method)(url=url,
                      headers=headers,
                      proxies=proxies,
                      verify=not mitmproxied)
