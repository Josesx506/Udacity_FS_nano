from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')
# SQLite doesn't require a username and password
JWT_SECRET = os.environ.get("JWT_SECRET")
LOG_LEVEL = os.environ.get("LOG_LEVEL")