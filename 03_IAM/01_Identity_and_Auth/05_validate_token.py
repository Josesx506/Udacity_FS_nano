# This script combines steps 03 and 04 by showing how the retrieved Auth0 token can be validated
from flask import Flask, abort, request
from functools import wraps
from jose import jwt
import json
from urllib.request import urlopen

# Configuration. 
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'dev-ehgjons8p0spxtoc.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'


class AuthError(Exception):
    '''Class to handle errors'''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Fucntion to verify the Auth0 token
def verify_decode_jwt(token):
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
                         'description': 'Authorization malformed.'}, 401)

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
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
        
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def get_token_auth_header():
    '''
    Function to extract the jwt token from a request header
    This function can be included in different endpoint functions,
    however, it'll be easier to implement it as a custom decorator
    that can be implemented above each endpoint
    '''

    # check if `authorization` key is in the request header
    if 'Authorization' in request.headers:
        # Unpack the request header  
        auth_header = request.headers['Authorization']
        # Split the `Bearer` string from the token
        header_parts = auth_header.split(' ')

        # check if token has 2 parts after the split for validation
        if len(header_parts) != 2:
            abort(401)
        
        # check that the first part of the split file equals 'Bearer'
        elif header_parts[0].lower() != 'bearer':
            abort(401)
        
        # If it passed all the previous checks extract the token value
        else:
            # get the token 
            header_token = header_parts[1]
    
    else:
        abort(401)

    return header_token


# Create the custom decorator
def requires_auth(f):
    '''This function will return the wrapper'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        '''
        The wrapper can accept multiple arguments. For now it is set up to 
        extract the jwt from the request header and return it to the decorator
        '''
        req_token = get_token_auth_header()
        try:
            payload = verify_decode_jwt(req_token)
        except:
            abort(401)
        return f(payload, *args, **kwargs)
    return wrapper




# ----------------------------------------------- Create the flask app -----------------------------------------------
app = Flask(__name__)

@app.route('/headers')
@requires_auth          # Custom decorator to get jwt token that can be repeated across multiple endpoints
def headers(validated_payload):
    print(validated_payload)
    return 'not implemented'


if __name__ == '__main__':
   app.debug = True
   app.run() #host="0.0.0.0", port=3000