import json
from flask import request,session
from functools import wraps
from jose import jwt
import os
from urllib.request import urlopen
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from settings import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
Implement get_token_auth_header() method
It should attempt to get the authorization token from the 
    session user. It should raise an AuthError if no session is present
    or if the token is malformed. It returns the token
'''
def get_token_auth_header():
    '''
    Function to extract the header token from a request. This function can 
    be included in different endpoint functions, however, it is implemented 
    as a custom decorator for easy usage above each endpoint
    '''
    # Check if the user has a valid session
    if session.get('user'):
        # Unpack the request header  
        
        # get the token 
        if 'access_token' in session.get('user'):
            header_token = session.get('user').get('access_token')
        
        # If it passed all the previous checks extract the token value
        else:
            raise AuthError({'code': 'invalid_authorization',
                            'description': 'User authorization session malformed.'}, 401)
        
    elif 'Authorization' in request.headers:
            # Unpack the request header  
            auth_header = request.headers['Authorization']
            # Split the `Bearer` string from the token
            header_parts = auth_header.split(' ')

            # check if token has 2 parts after the split for validation
            if len(header_parts) != 2:
                raise AuthError({'code': 'invalid_header',
                                'description': 'Authorization Header malformed 1.'}, 401)
            
            # check that the first part of the split file equals 'Bearer'
            elif header_parts[0].lower() != 'bearer':
                raise AuthError({'code': 'invalid_header',
                                'description': 'Authorization Bearer malformed 2.'}, 401)
            
            # If it passed all the previous checks extract the token value
            else:
                # get the token 
                header_token = header_parts[1]
    
    else:
        raise AuthError({'code': 'invalid_session',
                         'description': 'Verified user session is not identified or request header is invalid.'}, 401)
    
    return header_token
    

'''
Implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:bookings')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    '''
    The function checks that the specified user permission matches the required permission
    for an endpoint befor granting access
    '''
    # Check that the payload has a permission key
    if 'permissions' not in payload:
        raise AuthError({'code': 'invalid_claims',
                         'description': 'Permissions not included in JWT.'
                         }, 400)
    # Check that the user permission specified matches the one in the payload
    elif permission not in payload['permissions']:
        raise AuthError({'code': 'unauthorized',
                         'description': 'Permission not found.'
                         }, 403)
    else:
        return True

'''
Implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    '''
    This function validates an existing json web token
    '''
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    # Check that our key id is embedded within the token file
    if 'kid' not in unverified_header:
        # Raise a 401 error if it isn't included
        raise AuthError({'code': 'invalid_header',
                         'description': 'Authorization malformed 4. This token dies not have a valid `kid`'}, 401)

    # If it is included, format it properly
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            # Create an rsa key
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
                }
    
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer=f'https://{AUTH0_DOMAIN}/'
                                 )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({'code': 'token_expired',
                             'description': 'Token expired.'
                             }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({'code': 'invalid_claims',
                             'description': 'Incorrect claims. Please, check the audience and issuer.'
                             }, 401)
        
        except Exception:
            raise AuthError({'code': 'invalid_header',
                             'description': 'Unable to parse authentication token.'
                             }, 400)
        
    raise AuthError({'code': 'invalid_header',
                     'description': 'Unable to find the appropriate key.'
                     }, 400)

'''
Implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:bookings')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator