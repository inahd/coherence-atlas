import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("/opt/atlas/.env")

client = OpenAI()
DEFAULT_MODEL = os.environ.get("ATLAS_OPENAI_MODEL", "gpt-4o-mini")

def ask(prompt: str, model: str | None = None) -> str:
    model = model or DEFAULT_MODEL
    resp = client.responses.create(model=model, input=prompt)
    return resp.output_text
