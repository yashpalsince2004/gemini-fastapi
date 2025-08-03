from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# 🔷 Put your Gemini API key here only once
GEMINI_API_KEY = "AIzaSyAgDrb7ZK7bS6tEnzT5VnwjyWR_FWV1NIU"

# 🔷 Gemini API endpoint
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"

# 🔷 Define the expected request body
class ChatRequest(BaseModel):
    message: str

# 🔷 Define the /chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, json=payload)

    print("\n--- Gemini API raw response (text) ---")
    print(response.text)
    print("-------------------------------\n")

    try:
        gemini_reply = response.json()
    except Exception as e:
        print("Failed to parse JSON:", e)
        return {"reply": "Invalid response from Gemini."}

    if "error" in gemini_reply:
        error_message = gemini_reply["error"].get("message", "Unknown error from Gemini.")
        return {"reply": f"Gemini Error: {error_message}"}

    try:
        reply_text = gemini_reply["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error parsing Gemini response:", e)
        reply_text = "Sorry, could not parse Gemini's response."

    return {"reply": reply_text}

# uvicorn main:app --host 0.0.0.0 --port 8000 # To run the server, use the command above in your terminal
# Make sure to install FastAPI and Uvicorn if you haven't already:
# pip install fastapi uvicorn requests pydantic