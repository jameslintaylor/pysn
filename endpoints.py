from moya import Endpoint, HTTPMethod

class AuthEndpoint(Endpoint):
    sso = 1
    token = 2

    @property
    def url(self):
        return 'https://auth.api.sonyentertainmentnetwork.com/2.0' + {
            AuthEndpoint.sso: '/ssocookie',
            AuthEndpoint.token: '/oauth/token'
        }.get(self)

    @property
    def method(self):
        return {
            AuthEndpoint.sso: HTTPMethod.post_form,
            AuthEndpoint.token: HTTPMethod.post_form
        }.get(self)

    @property
    def parameters(self):
        def token_grant_parameters():
            if hasattr(self, 'refresh_token'):
                return {
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token
                }
            if hasattr(self, 'npsso'):
                return {
                    'grant_type': 'sso_cookie',
                    'npsso': self.npsso
                }

        return {
            AuthEndpoint.sso: \
            lambda: {
                'authentication_type': 'password',
                'username': self.username,
                'password': self.password,
                'client_id': '71a7beb8-f21a-47d9-a604-2e71bee24fe0'
            },
            AuthEndpoint.token: \
            lambda: {
                'client_id': '4db3729d-4591-457a-807a-1cf01e60c3ac',
                'client_secret': 'criemouwIuVoa4iU',
                'scope': 'user:account.get',
                **token_grant_parameters()
            }
        }.get(self, lambda: None)()

class AuthEndpointFactory:
    @classmethod
    def sso(cls, username, password):
        endpoint = AuthEndpoint.sso
        endpoint.username = username
        endpoint.password = password
        return endpoint

    @classmethod
    def token(cls, refresh_token=None, npsso=None):
        endpoint = AuthEndpoint.token
        if refresh_token:
            endpoint.refresh_token = refresh_token
        elif npsso:
            endpoint.npsso = npsso
        else:
            print("warning: token endpoint created without refresh_token or npsso!")
        return endpoint

class UserEndpoint(Endpoint):
    profile = 1
    friends = 2

    @property
    def url(self):
        return 'https://ca-prof.np.community.playstation.net/userProfile/v1/users/me' + {
            UserEndpoint.profile: '/profile2',
            UserEndpoint.friends: '/friends/profiles2'
        }.get(self)

    @property
    def method(self):
        return {
            UserEndpoint.profile: HTTPMethod.get,
            UserEndpoint.friends: HTTPMethod.get
        }.get(self)

    @property
    def parameters(self):
        return {
            UserEndpoint.profile: \
            lambda: {
                'fields': 'onlineId,presences(@titleInfo)'
            },
            UserEndpoint.friends: \
            lambda: {
                'limit': 16,
                'fields': 'onlineId,presences(@titleInfo)',
                'sort': 'onlineStatus'
            }
        }.get(self, lambda: None)()

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

class UserEndpointFactory:
    @classmethod
    def profile(cls, access_token):
        endpoint = UserEndpoint.profile
        endpoint.access_token = access_token
        return endpoint

    @classmethod
    def friends(cls, access_token):
        endpoint = UserEndpoint.friends
        endpoint.access_token = access_token
        return endpoint
