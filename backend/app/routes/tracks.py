# from fastapi import APIRouter, Query
# from app.services.spotify_api import get_recently_played

# router = APIRouter()

# @router.get("/recent-tracks")
# def recent_tracks(access_token: str = Query(...)):
#     try:
#         tracks = get_recently_played(access_token)
#         return {"tracks": tracks}
#     except Exception as e:
#         return {"error": str(e)}


''' updating the corrent code
to make it adaptive with
the issue of expiring token
automating the autorization 
to get new access token using refresh '''

from fastapi import APIRouter, Query
from app.services.spotify_api import get_recently_played, refresh_access_token
import os

router = APIRouter()

# Load refresh token from environment (or your DB)
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

@router.get("/recent-tracks")
def recent_tracks(access_token: str = Query(...), limit: int = 50):
    try:
        tracks = get_recently_played(access_token, limit)
        return {"tracks": tracks}
    except Exception as e:
        error_message = str(e).lower()

        # Check if token expired
        if "401" in error_message or "expired" in error_message:
            try:
                # Get new token
                new_access_token = refresh_access_token(REFRESH_TOKEN)

                # Retry fetching tracks with new token
                tracks = get_recently_played(new_access_token, limit)

                return {
                    "tracks": tracks,
                    "new_access_token": new_access_token
                }
            except Exception as refresh_err:
                return {"error": f"Token refresh failed: {refresh_err}"}

        return {"error": str(e)}



@router.get("/refresh_access_token")
def refresh_access_token_route():
    return refresh_access_token()