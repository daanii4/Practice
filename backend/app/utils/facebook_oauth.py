# Backend/app/utils/facebook_oauth.py
from fastapi import HTTPException
from authlib.integrations.requests_client import OAuth2Session
import os
from dotenv import load_dotenv

load_dotenv()

FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FACEBOOK_REDIRECT_URI = "http://localhost:3001/auth/facebook/callback"

def get_facebook_oauth_session():
    return OAuth2Session(
        client_id=FACEBOOK_APP_ID,
        client_secret=FACEBOOK_APP_SECRET,
        redirect_uri=FACEBOOK_REDIRECT_URI,
        scope="ads_management,email"
    )

def get_facebook_auth_url():
    facebook_session = get_facebook_oauth_session()
    authorization_url, state = facebook_session.authorization_url(
        "https://www.facebook.com/v12.0/dialog/oauth"
    )
    return authorization_url, state

def get_facebook_access_token(code: str):
    facebook_session = get_facebook_oauth_session()
    try:
        token = facebook_session.fetch_token(
            "https://graph.facebook.com/v12.0/oauth/access_token",
            code=code
        )
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error obtaining access token from Facebook")
