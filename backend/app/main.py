# from fastapi import FastAPI
# from app import auth

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Spotify Mood Tracker Backend Running"}

# new updated code as follows
from fastapi import FastAPI
from app.auth import router as auth_router
from app.routes.tracks import router as tracks_router
from fastapi.staticfiles import StaticFiles

from app.mood_predictor import router as mood_router

#from app.mood_predictor import predict_mood

app = FastAPI()

# @app.get("/get_moods")
# def get_moods(access_token: str):
#     moods = predict_mood(access_token)
#     return {"moods": moods}



# app.include_router(tracks_router)


app = FastAPI()

# app.include_router(auth_router)
# app.include_router(tracks_router)


app.include_router(auth_router, prefix="/auth")
app.include_router(tracks_router, prefix="/tracks")

app.include_router(mood_router, prefix="/moods")


@app.get("/")
def read_root():
    return {"message": "Spotify Mood Tracker Backend Running"}



# @app.get("/moods")
# def get_moods(access_token: str):
#     moods = predict_mood(access_token)
#     return {"moods": moods}

'''index.html d=frondend integration'''
app.mount("/static", StaticFiles(directory="app/static"), name="static")