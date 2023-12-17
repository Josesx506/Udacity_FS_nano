from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../../.env')
# SQLite doesn't require a username and password
DB_NAME = os.environ.get("DB_NAME")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = [os.environ.get("AUTH0_ALGORITHMS")]
API_AUDIENCE = os.environ.get("AUTH0__AUDIENCE")