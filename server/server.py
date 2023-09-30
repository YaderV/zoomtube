import base64
import os
from urllib.parse import urlencode, urljoin

import requests
from fastapi import FastAPI

app = FastAPI()

AUTH_URL = "https://zoom.us/oauth/authorize"
TOKEN_URL = "https://zoom.us/oauth/token"
API_URL = "https://api.zoom.us/"
U_REC_LIST_ENDPOINT = "/v2/users/me/recordings" # user recording list

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
    redirect_uri = os.getenv("ZOOM_REDIRECT_URL", "")
    if redirect_uri == "":
        return {"Error": "No ZOOM_REDIRECT_URL found in .env file"}

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }
    return requests.post(TOKEN_URL, auth=auth, data=data).json()

@app.get("/zoom/list")
def zomm_list(meeting_id: str = "", from_date: str = "", to_date: str = ""):
    zoom_token = os.getenv("ZOOM_TOKEN", "")
    if zoom_token == "":
        return {"Error": "No ZOOM_TOKEN found in .env file"}
    base_url = urljoin(API_URL, U_REC_LIST_ENDPOINT)
    params = {}
    if meeting_id != "":
        params["meeting_id"] = meeting_id
    if from_date != "":
        params["from_date"] = from_date
    if to_date != "":
        params["to_date"] = to_date
    url = f"{base_url}?{urlencode(params)}"
    return requests.get(url, headers={"Authorization": f"Bearer {zoom_token}"}).json()
