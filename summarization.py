from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Ensure OpenAI API key is set from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

class SummarizationRequest(BaseModel):
    text: str
    length: str = "short"  # short, medium, long

@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Missing OpenAI API Key")

    try:
        client = openai.OpenAI()  # ✅ Correct way to initialize the OpenAI client
        response = client.chat.completions.create(  # ✅ New API call format
            model="gpt-4o",  # ✅ Change from "gpt-4" to "gpt-4o"
            messages=[
                {"role": "system", "content": "You are an AI assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this in a {request.length} way: {request.text}"}
            ]
        )
        return {"summary": response.choices[0].message.content}
    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
