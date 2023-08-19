import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

URL = os.getenv("URL", "secret")
API_TOKEN = os.getenv("API_TOKEN", "secret")
