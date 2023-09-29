## Zoomtube

Zoomtube is a CLI tool aimed to download video recordings from zoom cloud and easily upload them to youtube.

### Connect to ZOOM
 - Create an zoom application and store the `client_id` and `client_secret` values in `.env` file.
 - Set `ZOOM_REDIRECT_URL` in the `.env` file. You can use a ssh tunnel like ngrok if you are working locally.
 - Run the `docker compose up -d` and go to `<url>/zoom/url`. You will get the zoom authorization url. Grant permission.
 - You will get the zoom `token` and `refresh_token` values. Store it in the `.env` file. Now you are ready to use the CLI.

