import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("🔍 Scanning available models...")
try:
    # פשוט מדפיס את השם של כל מודל שנמצא
    for model in client.models.list():
        print(f"✅ Found: {model.name}")
except Exception as e:
    print(f"❌ Error: {e}")