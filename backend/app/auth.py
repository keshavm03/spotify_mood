from fastapi import APIRouter, Request, Response, HTTPException, Query
import requests
from urllib.parse import urlencode
from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
import urllib.parse

from fastapi.responses import RedirectResponse

router = APIRouter()

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
HOME_PAGE_URL = "http://localhost:8000/static/home.html"


SCOPES = "user-read-recently-played user-read-email user-read-private"

@router.get("/login")
def login():
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPES,
        "show_dialog": "true"
    }
    url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return Response(status_code=302, headers={"Location": url})


# @router.get("/callback")
# def callback(code: str = None, error: str = None):
#     if error:
#         raise HTTPException(status_code=400, detail=f"Error during authorization: {error}")
#     if not code:
#         raise HTTPException(status_code=400, detail="No authorization code provided.")

#     # Exchange code for access and refresh tokens
#     payload = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": SPOTIFY_REDIRECT_URI,
#         "client_id": SPOTIFY_CLIENT_ID,
#         "client_secret": SPOTIFY_CLIENT_SECRET
#     }

#     response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Failed to get tokens from Spotify")

#     token_data = response.json()
#     access_token = token_data["access_token"]
#     refresh_token = token_data.get("refresh_token")

#     # TODO: Store tokens in DB or session associated with user

#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": token_data["token_type"],
#         "expires_in": token_data["expires_in"]
#     }


"""editing the above working code to integrate
login seamlessly, currenty the issue with login is that
we login and stuch on the callback page without gatting the access 
token, we tackel this problem by redirecting us"""



# @router.get("/callback")
# def callback(code: str = None, error: str = None):
#     if error:
#         raise HTTPException(status_code=400, detail=f"Error during authorization: {error}")
#     if not code:
#         raise HTTPException(status_code=400, detail="No authorization code provided.")

#     # Exchange code for tokens
#     payload = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": SPOTIFY_REDIRECT_URI,
#         "client_id": SPOTIFY_CLIENT_ID,
#         "client_secret": SPOTIFY_CLIENT_SECRET
#     }

#     response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Failed to get tokens from Spotify")

#     token_data = response.json()
#     access_token = token_data["access_token"]

#     # Optional: store refresh_token somewhere for later use
#     # refresh_token = token_data.get("refresh_token")

#     # Redirect back to home page with access_token in query params
#     redirect_url = f"/?access_token={urllib.parse.quote(access_token)}"
#     return RedirectResponse(url=redirect_url)



@router.get("/callback")
def callback(code: str = None, error: str = None):
    if error:
        raise HTTPException(status_code=400, detail=f"Error during authorization: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided.")

    # Exchange code for access and refresh tokens
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get tokens from Spotify")

    token_data = response.json()
    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")

    # Encode tokens in query params so frontend can grab them
    query_params = urllib.parse.urlencode({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": token_data["expires_in"]
    })

    # Redirect to home page with tokens
    return RedirectResponse(url=f"{HOME_PAGE_URL}?{query_params}")


# @router.get("/refresh-token")
# def refresh_token(refresh_token: str = Query(...)):
#     payload = {
#         "grant_type": "refresh_token",
#         "refresh_token": refresh_token,
#         "client_id": SPOTIFY_CLIENT_ID,
#         "client_secret": SPOTIFY_CLIENT_SECRET,
#     }
#     response = requests.post(SPOTIFY_TOKEN_URL, data=payload)
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")

#     token_data = response.json()
#     return {
#         "access_token": token_data["access_token"],
#         "token_type": token_data.get("token_type"),
#         "expires_in": token_data.get("expires_in"),
#         # Spotify may or may not return a new refresh_token here
#         "refresh_token": token_data.get("refresh_token", refresh_token)
#     }



@router.get("/refresh-token")
def refresh_token(refresh_token: str):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    response = requests.post(token_url, data=payload)
    return response.json()
