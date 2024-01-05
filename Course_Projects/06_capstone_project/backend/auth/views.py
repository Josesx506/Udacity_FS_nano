from authlib.integrations.flask_client import OAuth
from flask import Blueprint, current_app, redirect, session, url_for
import os
from urllib.parse import quote_plus, urlencode
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from settings import CLIENT_ID, CLIENT_SECRET, AUTH0_DOMAIN, API_AUDIENCE


auth_bp = Blueprint('auth', __name__)
oauth = OAuth(current_app)


domain = AUTH0_DOMAIN
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
audience = API_AUDIENCE

# Register the auth0 app
oauth.register(
    "auth0",
    client_id=client_id,
    client_secret=client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{domain}/.well-known/openid-configuration'
)

# -------------------------------------------------------- CALLBACK --------------------------------------------------------
# Create a callback endpoint that redirects the user to the home page
@auth_bp.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    session["role"] = token['userinfo'][f'{domain}/roles'][0]
    # This app assumes for a /appointments path to be available, change here if it's not
    return redirect("/home")


# -------------------------------------------------------- LOG IN --------------------------------------------------------
@auth_bp.route("/login")
def login():
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    If the audience is not provided, the key is not valid
    authorization': 'Bearer {}'.format(access_token)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True),
        audience=audience
    )

# ------------------------------------------------------- LOG OUT -------------------------------------------------------
@auth_bp.route("/logout")
def logout():
    """
    Logs the user out of the session and from the Auth0 tenant
    """
    session.clear()
    return redirect(f"https://{domain}/v2/logout?"
        + urlencode({"returnTo": url_for("index", _external=True),
                     "client_id": client_id,}, quote_via=quote_plus,)
    )