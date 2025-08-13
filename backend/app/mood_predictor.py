# # mood_predictor.py
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from fastapi import APIRouter, Query, HTTPException
# from typing import List, Dict
# import datetime
# import importlib.metadata
# import requests

# router = APIRouter()

# def classify_mood(valence, energy):
#     """Classify mood based on valence & energy values."""
#     if valence > 0.7 and energy > 0.6:
#         return "Happy & Energetic"
#     elif valence > 0.7:
#         return "Happy & Calm"
#     elif valence < 0.3 and energy > 0.6:
#         return "Angry / Tense"
#     elif valence < 0.3:
#         return "Sad & Calm"
#     else:
#         return "Neutral / Mixed"

# @router.get("/get_moods")
# def get_moods(access_token: str = Query(...)):
#     try:
#         sp = spotipy.Spotify(auth=access_token)
#         results = sp.current_user_recently_played(limit=10)

#         moods_data = []

#         for item in results['items']:
#             track = item['track']
#             played_at = item['played_at']  # ISO timestamp
#             audio_features = sp.audio_features(track['id'])[0]

#             if audio_features:
#                 valence = audio_features['valence']
#                 energy = audio_features['energy']
#                 mood = classify_mood(valence, energy)

#                 # Convert timestamp to human-readable time
#                 time_str = datetime.datetime.fromisoformat(played_at.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S")

#                 moods_data.append({
#                     "time": time_str,
#                     "mood": mood
#                 })

#         return {"moods": moods_data}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# #print(importlib.metadata.version("spotipy"))

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict
import datetime
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)


def classify_mood(valence, energy):
    """Classify mood based on valence & energy values."""
    if valence > 0.7 and energy > 0.6:
        return "Happy & Energetic"
    elif valence > 0.7:
        return "Happy & Calm"
    elif valence < 0.3 and energy > 0.6:
        return "Angry / Tense"
    elif valence < 0.3:
        return "Sad & Calm"
    else:
        return "Neutral / Mixed"


@router.get("/get_moods")
def get_moods(access_token: str = Query(...)):
    try:
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user_recently_played(limit=50)
        moods_data = []

        for item in results.get('items', []):
            track = item.get('track')
            played_at = item.get('played_at')

            # Skip unsupported items
            if not track or track.get('type') != 'track':
                moods_data.append({
                    "time": played_at,
                    "mood": "Unsupported track / podcast / ad"
                })
                continue

            try:
                audio_features = sp.audio_features(track['id'])[0]
            except SpotifyException as se:
                logging.warning(f"Audio features fetch failed for track {track.get('id')}: {se}")
                moods_data.append({
                    "time": played_at,
                    "mood": "Audio features unavailable"
                })
                continue

            if not audio_features:
                moods_data.append({
                    "time": played_at,
                    "mood": "Audio features missing"
                })
                continue

            valence = audio_features.get('valence')
            energy = audio_features.get('energy')

            if valence is None or energy is None:
                moods_data.append({
                    "time": played_at,
                    "mood": "Audio features incomplete"
                })
                continue

            mood = classify_mood(valence, energy)
            time_str = datetime.datetime.fromisoformat(
                played_at.replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M:%S")

            moods_data.append({
                "time": time_str,
                "mood": mood
            })

        return {"moods": moods_data}

    except SpotifyException as se:
        logging.error(f"Spotify API error: {se}")
        if se.http_status == 401:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        raise HTTPException(status_code=500, detail=f"Spotify API error: {se}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

