import os
from urllib.parse import urlencode

import requests
from fastapi import FastAPI

app = FastAPI()

AUTH_URL = "https://zoom.us/oauth/authorize"
TOKEN_URL = "https://zoom.us/oauth/token"

@app.get("/zoom/url")
def zoom_url():
    client_id = os.getenv("ZOOM_CLIENT_ID", "")
    if client_id == "":
        return {"Error": "No ZOOM_CLIENT_ID found in .env file"}
    redirect_uri = os.getenv("ZOOM_REDIRECT_URL", "")
    if redirect_uri == "":
        return {"Error": "No ZOOM_REDIRECT_URL found in .env file"}
    params = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri}
    return {"url": f"{AUTH_URL}?{urlencode(params)}"}


@app.get("/zoom/connect")
def zoom_connect(code: str):
    client_id = os.getenv("ZOOM_CLIENT_ID", "")
    if client_id == "":
        return {"Error": "No ZOOM_CLIENT_ID found in .env file"}
    client_secret = os.getenv("ZOOM_CLIENT_SECRET", "")
    if client_secret == "":
        return {"Error": "No ZOOM_CLIENT_SECRET found in .env file"}
    headers = {
        "Authorization": f"{client_id}:{client_secret}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    return requests.post(TOKEN_URL, headers=headers).json()

