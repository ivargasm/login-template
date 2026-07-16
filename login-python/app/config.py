import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = os.getenv("SCHEMA", "public")  # Default to 'public' if not set

# secretkey
SECRET_KEY = os.getenv("SECRET_KEY")

# datos de correo
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

# Resend & Frontend Config
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_MAIL_FROM = os.getenv("RESEND_MAIL_FROM")
URL_FRONT = os.getenv("URL_FRONT", "http://localhost:3000")

# tiempo de expiracion de tokens
SESSION_EXPIRE_MINUTES = os.getenv("SESSION_EXPIRE_MINUTES")