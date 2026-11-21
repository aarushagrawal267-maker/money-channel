"""One-time YouTube authorization. Run this on YOUR OWN computer, not in the cloud session.

1. Install Python 3 from python.org (tick "Add Python to PATH" on Windows).
2. Put this file and the client_secret.json you downloaded from Google Cloud in the same folder.
3. In that folder, run:
       pip install google-auth-oauthlib
       python get_youtube_token.py
4. A browser opens. Log in with the channel's Google account and, when asked,
   pick the CHANNEL (brand account), not your personal profile. If you see
   "Google hasn't verified this app", click Advanced -> Go to (your app name).
5. The script prints three values. Save them in your Claude cloud environment
   settings as environment variables (never paste them into the chat).
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",        # upload videos + thumbnails
    "https://www.googleapis.com/auth/youtube.readonly",      # read channel/video stats
    "https://www.googleapis.com/auth/yt-analytics.readonly", # analytics to tune upload times
]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

print("\nSave these as environment variables in your Claude cloud environment:\n")
print("YT_CLIENT_ID     =", creds.client_id)
print("YT_CLIENT_SECRET =", creds.client_secret)
print("YT_REFRESH_TOKEN =", creds.refresh_token)
print("\nKeep them private. Do not share them in chat or commit them to GitHub.")
