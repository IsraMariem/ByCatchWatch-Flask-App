import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+pg8000://myuser:isra@localhost/bycatchdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False



