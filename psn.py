from datetime import datetime, timedelta
from functools import wraps

from .moya import Provider
from .endpoints import AuthEndpointFactory, UserEndpointFactory

class PSNError(BaseException):
    """wraps the json style errors returned by the psn api"""
    def __init__(self, json):
        try:
            self.code = json['error_code']
            self.description = json['error_description'].lower()
        except KeyError:
            raise PSNError.InitializationError()

    class InitializationError(BaseException):
        pass

class PSNToken:
    """wraps an access/refresh tokens needed to interact with the psn api"""
    def __init__(self, value, expiry_date):
        self.value = value
        self.expiry_date = expiry_date

    @property
    def is_expired(self):
        return self.expiry_date < datetime.now()

def get_sso(username, password):
    """gets an sso key from psn using the provided credentials"""
    endpoint = AuthEndpointFactory.sso(username, password)
    json = Provider().request(endpoint).json()
    try:
        return json['npsso']
    except KeyError:
        raise PSNError(json)

def get_tokens(sso):
    """given an sso, gets an api access token and refresh token from psn.
    note that the refresh token might be None"""
    endpoint = AuthEndpointFactory.token(npsso=sso)
    json = Provider().request(endpoint).json()
    # parse tokens from response json
    try:
        access_value = json['access_token']
        access_expiry = datetime.now() + timedelta(seconds=json['expires_in'])
        access_token = PSNToken(access_value, access_expiry)
        # the lack of a refresh token shouldn't cause an error
        if 'refresh_token' in json:
            refresh_value = json['refresh_token']
            refresh_expiry = datetime.now() + timedelta(seconds=3600*24*14) # 2 weeks
            refresh_token = PSNToken(refresh_value, refresh_expiry)
            return access_token, refresh_token
        else:
            return access_token, None
    except KeyError:
        raise PSNError(json)

def get_friends(access_token):
    """given an access token, get the friends list of the user it is authorized
    to. if no errors present, return psn's exact response"""
    if access_token.is_expired:
        print("access_token is expired! can't get friends :(")
        return
    endpoint = UserEndpointFactory.friends(access_token=access_token.value)
    return _catch_error_or_relay(endpoint)

def get_profile(access_token):
    """given an access token, get the profile for the user it is authorized
    to. if no errors present, return psn's exact response"""
    if access_token.is_expired:
        print("access_token is expired! can't get profile :(")
        return
    endpoint = UserEndpointFactory.profile(access_token=access_token.value)
    return _catch_error_or_relay(endpoint)

def _catch_error_or_relay(endpoint):
    """requests the endpoint provided and checks for any errors in the response.
    if no errors present, this method returns psn's exact response"""
    json = Provider().request(endpoint).json()
    try:
        # check if the response is an error. if so raise it
        raise PSNError(json)
    except PSNError.InitializationError:
        # otherwise simply pass back the json response returned from psn
        return json
