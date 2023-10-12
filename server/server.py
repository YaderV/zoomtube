import os
from urllib.parse import urlencode, urljoin

import requests
from fastapi import FastAPI

app = FastAPI()

AUTH_URL = "https://zoom.us/oauth/authorize"
TOKEN_URL = "https://zoom.us/oauth/token"
API_URL = "https://api.zoom.us/"
U_MEETING_LIST_EP = "/v2/users/me/meetings"
U_MEETING_REC_EP = "/v2/meetings/{meeting_id}/recordings"
REC_FILE_TYPE = "MP4"

@app.get("/zoom/url")
def zoom_url():
    client_id = os.getenv("ZOOM_CLIENT_ID", "")
    if client_id == "":
        return "Error: No ZOOM_CLIENT_ID found in .env file"
    redirect_uri = os.getenv("ZOOM_REDIRECT_URL", "")
    if redirect_uri == "":
        return "Error: No ZOOM_REDIRECT_URL found in .env file"
    params = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri}
    return f"URL: {AUTH_URL}?{urlencode(params)}"


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

@app.get("/zoom/meetings")
def zoom_meeting():
    zoom_token = os.getenv("ZOOM_TOKEN", "")
    base_url = urljoin(API_URL, U_MEETING_LIST_EP)
    resp = requests.get(base_url, headers={"Authorization": f"Bearer {zoom_token}"}).json()
    try:
        data = []
        for meeting in resp["meetings"]:
            m = {"name": meeting["topic"], "id": meeting["id"]}
            data.append(m)
        return data

    except KeyError:
        if 'message' in resp:
            return f"Error: {resp['message']}"

    return "Unexpected error happened"



@app.get("/zoom/meetings/{meeting_id}")
def zoom_meeting_rec(meeting_id):
    zoom_token = os.getenv("ZOOM_TOKEN", "")
    path = U_MEETING_REC_EP.replace("{meeting_id}", meeting_id)
    base_url = urljoin(API_URL, path)
    resp = requests.get(base_url, headers={"Authorization": f"Bearer {zoom_token}"}).json()
    try:
        if "topic" not in resp:
            # TODO: we are hidden errors
            return "Error: No recording"

        data = {"name": resp["topic"]}
        rec_list = []
        for rec in resp["recording_files"]:
            if rec["file_type"] == REC_FILE_TYPE:
                r = {"date": rec["recording_start"], "url": rec["download_url"]}
                rec_list.append(r)
        data["recordings"] = rec_list
        return data

    except KeyError:
        if 'message' in resp:
            return f"Error: {resp['message']}"

    return "Unexpected error happened"
