from jose import jwt
import sys
import time

# Append the directory above to enable imports
sys.path.append("..")

# Import app and model dependencies
from settings import AUTH0_DOMAIN, CLIENT_SECRET, CLIENT_ID, ADMIN_USER_ID, ADMIN_ROLE, CUSTOMER_USER_ID, CUSTOMER_ROLE

admin_permissions = ['delete:adminbookings','delete:bookings','delete:services','delete:stylists','get:bookings',
                     'get:services','get:stylists','patch:bookings','post:bookings','post:services','post:stylists']
customer_permissions = ['delete:bookings','get:bookings','get:services','get:stylists','patch:bookings','post:bookings']

def generate_auth0_token(roles, user_id, user_permissions):
    # Define token expiration time (e.g., 1 hour)
    expiration_time = int(time.time()) + 3600

    # Auth0 token claims
    claims = {
        "sub": user_id,
        "aud": CLIENT_ID,
        "exp": expiration_time,
        "iss": f"https://{AUTH0_DOMAIN}/",
        "roles": roles,  # Include user roles in the token
        "permissions": user_permissions
    }

    # Generate the Auth0 token
    token = jwt.encode(claims, CLIENT_SECRET, algorithm='HS256')

    return token


# Example: Generate tokens for users with different roles
admin_token = generate_auth0_token(roles=ADMIN_ROLE,user_id=ADMIN_USER_ID,user_permissions=admin_permissions)
user_token = generate_auth0_token(roles=CUSTOMER_ROLE,user_id=CUSTOMER_USER_ID,user_permissions=customer_permissions)

# print("Admin Token:", admin_token)
# print("User Token:", user_token)