from moya import Endpoint, HTTPMethod

## AUTHENTICATION

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
                'grant_type': 'sso_cookie',
                'npsso': self.npsso,
                'scope': 'user:account.get'
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
    def token(cls, npsso):
        endpoint = AuthEndpoint.token
        endpoint.npsso = npsso
        return endpoint

## USER

class UserEndpoint(Endpoint):
    profile = 1
    friends = 2

    @property
    def url(self):
        base = 'https://ca-prof.np.community.playstation.net/userProfile/v1/users/{}' \
                .format(self.user)
        return base + {
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
            UserEndpoint.friends: \
            lambda: {
                'limit': 16,
                'fields': 'onlineId,presences(@titleInfo)',
                'sort': 'onlineStatus',
                'avatarSizes': 'm',
                'profilePictureSizes': 'm'
            }
        }.get(self, lambda: None)()

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

class UserEndpointFactory:
    @classmethod
    def friends(cls, user, access_token):
        endpoint = UserEndpoint.friends
        endpoint.user = user
        endpoint.access_token = access_token
        return endpoint
