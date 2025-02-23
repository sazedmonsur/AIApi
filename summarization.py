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
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        return content.strip()
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
        response = openai.ChatCompletion.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this in a {request.length} way: {content}"}
            ]
        )
        return {"summary": response["choices"][0]["message"]["content"]}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
