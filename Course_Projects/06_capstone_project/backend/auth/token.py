from datetime import datetime,timedelta
from flask import Blueprint, jsonify, request
from jose import jwt
import logging
import os
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from settings import LOG_LEVEL, LOCAL_SECRET_KEY


token_bp = Blueprint('token', __name__)

def _logger():
    '''
    Setup logger format, level, and handler.

    RETURNS: log object
    '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log

LOG = _logger()
log_level = getattr(logging, LOG_LEVEL.upper(), None)

if log_level is None:
    raise ValueError(f"Invalid log level: {LOG_LEVEL}")

LOG.setLevel(log_level)
LOG.debug("Starting with log level: %s" % LOG_LEVEL )

@token_bp.route('/auth', methods=['POST','GET'])
def auth():
    """
    Create JWT token based on email.
    """
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        LOG.error("No email provided")
        return jsonify({"message": "Missing parameter: email"}, 400)
    if not password:
        LOG.error("No password provided")
        return jsonify({"message": "Missing parameter: password"}, 400)
    body = {'email': email, 'password': password}

    user_data = body

    return jsonify(token=_get_jwt(user_data))


def _get_jwt(user_data):
    exp_time = datetime.utcnow() + timedelta(weeks=2)
    payload = {'exp': exp_time,
               'nbf': datetime.utcnow(),
               'email': user_data['email']}
    return jwt.encode(payload, LOCAL_SECRET_KEY, algorithm='HS256')