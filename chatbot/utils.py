import aiofiles
import os

HALLUCINATION_FILE = "hallucination_keywords.txt"
DEFAULT_KEYWORDS = ["you are", "scenario", "imagine", "consider"]

async def load_hallucination_keywords():
    if os.path.exists(HALLUCINATION_FILE):
        async with aiofiles.open(HALLUCINATION_FILE, mode='r') as f:
            return [line.strip().lower() for line in await f.readlines()]
    return DEFAULT_KEYWORDS

def contains_hallucination(text, keywords):
    text = text.strip().lower()
    return any(keyword in text for keyword in keywords)
