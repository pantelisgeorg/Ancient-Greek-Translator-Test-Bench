# Greek Translator Test Bench

A small web app for benchmarking LLM translation of Ancient Greek. It supports
multiple translation directions, editable system prompts (TranslatorMind-style),
side-by-side model comparison, and works with any OpenAI-compatible API.

## Features

- Auto-detect direction (English ↔ Attic Greek) plus explicit presets:
  Ancient Greek → Modern Greek (δημοτική), English → Attic Greek (polytonic),
  Ancient Greek → English
- Editable system prompts, saved per direction (localStorage)
- Side-by-side comparison of two models
- Custom base URL for OpenAI-compatible endpoints (OpenRouter, local vLLM, etc.)
- API key kept in the browser only (or fall back to `OPENAI_API_KEY` env var)
- Token usage and latency per response

## Setup

```bash
uv sync          # or: uv pip install .
uv run uvicorn app:app --reload
```

Open http://localhost:8000.

Alternatively, without uv:

```bash
pip install fastapi uvicorn openai
uvicorn app:app --reload
```

## Configuration

- **API key**: enter it in the browser (stored in localStorage only), or set
  `OPENAI_API_KEY` on the server.
- **Base URL**: defaults to `https://api.openai.com/v1`. Point it at any
  OpenAI-compatible endpoint.
- **Temperature**: default 0.2.

## API

`POST /api/translate`

```json
{
  "text": "πολλοὶ γὰρ καλεῖται, ὀλίγοι δὲ ἐκλέγονται.",
  "system_prompt": "You are an expert translator of Ancient Greek...",
  "model": "gpt-4o",
  "api_key": "sk-...",
  "base_url": "https://api.openai.com/v1",
  "temperature": 0.2
}
```

Returns `{ ok, output, model, elapsed_ms, usage, error }`.

## Project layout

- `app.py` — FastAPI backend with a single `/api/translate` endpoint
- `static/index.html` — self-contained frontend (no build step)
