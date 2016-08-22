from moya import Provider
from functools import wraps
from endpoints import AuthEndpointFactory, UserEndpointFactory

def get_npsso(username, password):
    """gets an sso key from psn using the provided credentials"""
    endpoint = AuthEndpointFactory.sso(username, password)
    resp = Provider().request(endpoint)
    return resp.json()['npsso']

class PSNSession:
    def __init__(self, npsso):
        self.npsso = npsso
        self.provider = Provider()

    def get_tokens(self):
        refresh_token = getattr(self, 'refresh_token', None)
        # npsso = getattr(self, 'npsso', None)
        # endpoint = AuthEndpointFactory.token(refresh_token=refresh_token,
        #                                      npsso=npsso)
        # resp = self.provider.request(endpoint)
        # self.access_token, self.refresh_token = parse_tokens(resp.json())

    def token_required(f):
        """decorator that enforces the presence of an access_token"""
        @wraps(f)
        def decorated(self, *args, **kwargs):
            if hasattr(self, 'access_token'):
                return f(self, *args, **kwargs)
            else:
                raise AttributeError("don't have an access token!")
        return decorated

    @token_required
    def get_profile(self):
        endpoint = UserEndpointFactory.profile(self.access_token.value)
        resp = self.provider.request(endpoint)
        return resp.json()

    @token_required
    def get_friends(self):
        endpoint = UserEndpointFactory.friends(self.access_token.value)
        resp = self.provider.request(endpoint)
        return resp.json()
