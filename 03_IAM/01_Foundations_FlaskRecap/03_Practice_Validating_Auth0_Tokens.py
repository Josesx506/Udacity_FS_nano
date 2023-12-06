import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

# Define a class to handle errors
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# PASTE YOUR OWN TOKEN HERE. This is obtained from Auth0 after a user has clicked login and 
# is redirected to our specified backend endpoint url
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims3VjJOd2V1TXQzc04xX3U3d2wteiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laGdqb25zOHAw\
    c3B4dG9jLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTZlY2M0YjgxMTdkYTBkOGI1MTdlNGYiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTcwMTg1Mzg3OC\
        wiZXhwIjoxNzAxODYxMDc4LCJhenAiOiJ4S3VWSUZibjhEUDdQTXZWYzhIR1lHdmJFZHRFazFuQSIsInNjb3BlIjoiIn0.aZWrVps98ISfctBhKbjJmYCTf\
            jrFs4rdwOFsadZR3mec8GUpdwsEAULfB1iwjUPan7gn4k-MYZlXWR3u3-C113BhiSCq2eIiOc0O3hmSIItoKSMj8BRjxL_m_LfG7xjcmwkkF0zaueJ2\
                iE0e8H2ezISLJUeWV0bM335OcLjCXFCWGonr8G_xxnLQtpt0IZ9gvSjvDAh7EZDp2AAfiWF442cC7UWPFRVqQIk_c-s-WS6UyJEpKs5igFTHTM8\
                    koof15a14yvbMPrKDWvkVpRHTe0-lNJ3km65Pb7ZvqydA0kjqxG7mMYI5IcdSiskoO7SfWUO_e2jnowkO-2nVnRvlpw"


# Fucntion to verify the Auth0 token
## Auth Header
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
                                 issuer='https://' + AUTH0_DOMAIN + '/'
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