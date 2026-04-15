import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, "instance")

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(INSTANCE_PATH, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")