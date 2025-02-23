from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import openai
import os
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Ensure OpenAI API key is set from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

class SummarizationRequest(BaseModel):
    text: str = None  # Optional if URL is provided
    url: HttpUrl = None  # Optional if text is provided
    length: str = "short"  # short, medium, long

def extract_text_from_url(url):
    """Fetch and extract main content from a webpage."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        # If the response is text/plain
        if "text/plain" in response.headers.get("Content-Type", "").lower():
            return response.text.strip()

        # If the response is HTML
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        return content.strip()

    except requests.Timeout:
        raise HTTPException(status_code=408, detail="Request to URL timed out.")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Missing OpenAI API Key")

    # Get content from either text input or URL
    content = request.text if request.text else extract_text_from_url(str(request.url))

    if not content:
        raise HTTPException(status_code=400, detail="No valid text found to summarize.")

    try:
        response = openai.chat.completions.create(  # ✅ FIXED: New API method
            model="gpt-3.5-turbo",  # Use a valid model from OpenAI
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this in a {request.length} way: {content}"}
            ]
        )
        return {"summary": response.choices[0].message.content}  # ✅ FIXED: New response structure

    except openai.OpenAIError as e:  # ✅ FIXED: Corrected exception handling
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
