import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Try printing the API key
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    print("✅ .env file loaded successfully.")
    print("GOOGLE_API_KEY:", google_api_key)
else:
    print("❌ Failed to load GOOGLE_API_KEY from .env file.")
