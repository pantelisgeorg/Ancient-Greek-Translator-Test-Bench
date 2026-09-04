import os
import time
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from pydantic import BaseModel

app = FastAPI(title="Greek Translator Test Bench")

DEFAULT_BASE_URL = "https://api.openai.com/v1"


class TranslateRequest(BaseModel):
    text: str
    system_prompt: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.2


class TranslateResponse(BaseModel):
    ok: bool
    output: Optional[str] = None
    model: Optional[str] = None
    elapsed_ms: Optional[int] = None
    usage: Optional[dict] = None
    error: Optional[str] = None


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    api_key = req.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=400, detail="No API key provided")
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    client = AsyncOpenAI(api_key=api_key, base_url=req.base_url or DEFAULT_BASE_URL)
    started = time.time()
    try:
        resp = await client.chat.completions.create(
            model=req.model,
            temperature=req.temperature,
            messages=[
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.text},
            ],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"API error: {exc}")

    elapsed_ms = int((time.time() - started) * 1000)
    return TranslateResponse(
        ok=True,
        output=resp.choices[0].message.content,
        model=resp.model,
        elapsed_ms=elapsed_ms,
        usage=resp.usage.model_dump() if resp.usage else None,
    )


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
    return FileResponse("static/index.html")
