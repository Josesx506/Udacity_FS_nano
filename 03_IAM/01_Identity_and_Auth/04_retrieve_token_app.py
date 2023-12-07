# Script to access token from request header with flask
from flask import Flask, abort, request
from functools import wraps

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
        jwt = get_token_auth_header()
        return f(jwt, *args, **kwargs)
    return wrapper

app = Flask(__name__)

@app.route('/headers')
@requires_auth          # Custom decorator to get jwt token that can be repeated across multiple endpoints
def headers(jwt):
    print(jwt)
    return 'not implemented'


if __name__ == '__main__':
   app.debug = True
   app.run() #host="0.0.0.0", port=3000