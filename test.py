from endpoints import AuthEndpointFactory, UserEndpointFactory
from moya import Provider

def npsso_request(session=None):
    endpoint = AuthEndpointFactory.sso(username='jameslintaylor@gmail.com',
                                       password='l4c5c49293')
    return Provider.request(endpoint, session=session, mitmproxied=True)

def token_request(npsso, session=None):
    endpoint = AuthEndpointFactory.token(npsso=npsso)
    return Provider.request(endpoint, session=session, mitmproxied=True)

def friends_request(user, access_token, session=None):
    endpoint = UserEndpointFactory.friends(user=user, access_token=access_token)
    return Provider.request(endpoint, session=session, mitmproxied=True)

r, s = npsso_request()
npsso = r.json()['npsso']
r, s = token_request(npsso, session=s)
r, s = friends_request('JiBBsTeRR', access_token=r.json()['access_token'], session=s)
