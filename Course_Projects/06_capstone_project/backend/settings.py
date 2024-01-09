from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')
# SQLite doesn't require a username and password
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO') # Default to 'INFO' if LOG_LEVEL is not set
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = [os.environ.get("AUTH0_ALGORITHMS")]
API_AUDIENCE = os.environ.get("AUTH0__AUDIENCE")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
LOCAL_SECRET_KEY = os.environ.get("LOCAL_SECRET_KEY")
ADMIN_USER_ID = os.environ.get("ADMIN_USER_ID")
ADMIN_ROLE = os.environ.get("ADMIN_ROLE")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
CUSTOMER_USER_ID = os.environ.get("CUSTOMER_USER_ID")
CUSTOMER_ROLE = os.environ.get("CUSTOMER_ROLE")
USER_TOKEN = os.environ.get("USER_TOKEN")