import os
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv("API_HOST")
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT"))