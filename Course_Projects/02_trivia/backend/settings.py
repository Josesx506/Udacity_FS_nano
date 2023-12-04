from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')
DB_NAME = os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")