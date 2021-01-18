import time

import boto3
import requests_oauthlib as rqo


redirect_uri = 'https://waterloorocketry.com/auth'

auth_base = 'https://launchpad.37signals.com/authorization'
auth_endpoint = f'{auth_base}/new?type=web_server'
token_endpoint = f'{auth_base}/token?type=web_server'
refresh_endpoint = f'{auth_base}/token?type=refresh'

headers = {
    'User-Agent': 'Aqueduct, by Waterloo Rocketry (contact@waterloorocketry.com)'
}


def save_token(token):
    ssm_client = boto3.client('ssm')
    
    ssm_client.put_parameter(Name='access', Value=token['access_token'], Overwrite=True)
    ssm_client.put_parameter(Name='refresh', Value=token['refresh_token'], Overwrite=True)


def make_session():
    ssm_client = boto3.client('ssm')

    # All tokens are stored in the AWS Systems Manager Parameter Store.
    access_token = ssm_client.get_parameter(Name='access')['Parameter']['Value']
    refresh_token = ssm_client.get_parameter(Name='refresh')['Parameter']['Value']
    client_id = ssm_client.get_parameter(Name='client_id')['Parameter']['Value']
    client_secret = ssm_client.get_parameter(Name='client_secret')['Parameter']['Value']

    # By setting expires_in to -1, we force a token refresh every time.
    # This isn't strictly necessary, since the token lasts for about 2
    # weeks, but it's easier than trying to keep track of expiry dates.
    token = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': -1
    }
    
    extra = {
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    sess = rqo.OAuth2Session(client_id, redirect_uri=redirect_uri, token=token,
                             auto_refresh_url=refresh_endpoint, auto_refresh_kwargs=extra,
                             token_updater=save_token)
    sess.headers.update(headers)

    return sess
