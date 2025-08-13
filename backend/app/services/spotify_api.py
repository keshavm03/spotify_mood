# import requests

# def get_recently_played(access_token, limit=20):
#     url = "https://api.spotify.com/v1/me/player/recently-played"
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
#     params = {"limit": limit}

#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code != 200:
#         raise Exception(f"Spotify API error: {response.status_code} {response.text}")

#     data = response.json()
#     items = data.get("items", [])
#     tracks = []
#     for item in items:
#         track = item["track"]
#         played_at = item["played_at"]
#         tracks.append({
#             "name": track["name"],
#             "artists": [artist["name"] for artist in track["artists"]],
#             "played_at": played_at
#         })
#     return tracks

'''to upgrade the change in the access toke
in case of expiry 
we need new token 
this update it to make it automate'''

import requests
from app.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN

def refresh_access_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Error refreshing token: {response.status_code} {response.text}")

    return response.json().get("access_token")

def get_recently_played(access_token, limit=20):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {"limit": limit}

    response = requests.get(url, headers=headers, params=params)

    # If token expired, refresh & retry once
    if response.status_code == 401:
        access_token = refresh_access_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Spotify API error: {response.status_code} {response.text}")

    data = response.json()
    items = data.get("items", [])
    tracks = []
    for item in items:
        track = item["track"]
        played_at = item["played_at"]
        tracks.append({
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "played_at": played_at
        })
    return tracks

