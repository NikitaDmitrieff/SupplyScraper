import os

from credentials import GOOGLE_API_KEY


def setup_google_api_key():
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
