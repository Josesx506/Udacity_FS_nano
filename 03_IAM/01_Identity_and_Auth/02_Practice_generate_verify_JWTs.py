### Practice - Generating and Verifying JWTs

# Import Python Package
import jwt
import base64

# Init our Data
payload = {'park':'madison square'} # JSON payload
algo = 'HS256'                      # HMAC-SHA 256 - Encoding algorithm
secret = 'learning'                 # Secret key

# Encode a JWT
encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(encoded_jwt)

# Decode a JWT
decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True, algorithms=algo)
print(decoded_jwt)

# Decode with Simple Base64 Encoding
decoded_base64 = base64.b64decode(str(encoded_jwt).split(".")[1]+"==")
print(decoded_base64)

# Encode any type of payload. It's the secret key that is important
print(jwt.encode({'school':'udacity'}, secret, algorithm=algo))

# Decode any token. This should throw an `InvalidSignatureError("Signature verification failed")` error
bad_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXJrIjoiYmF0dGVyeSBwYXJrIn0.bQEjsBRGfhKKEFtGhh83sTsMSXgSstFA_P8g2qV5Sns'
# print(jwt.decode(bad_token, secret, verify=True, algorithms=algo))

# If the wrong secret key is used, it'll throw a verification error