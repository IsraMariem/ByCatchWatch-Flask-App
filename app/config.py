import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+pg8000://myuser:isra@localhost/bycatchdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    CLIENT_ID = "370045102958-cpc6e3an5jkbeh81rcildhcg3vrjgi9l.apps.googleusercontent.com" 
    CLIENT_SECRET = "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"
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    API_BASE_URL = 'https://www.googleapis.com'
    REDIRECT_URI = 'http://localhost:5000/callback'  # Your redirect URI
