import os
import numpy as np
from openai import OpenAI
import imageio_ffmpeg

client = None

def get_client():
    global client
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    return client

def get_ffmpeg_path():
    """Returns the path to the ffmpeg executable."""
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg" # Fallback to system PATH


def get_embedding(text: str) -> list[float]:
    """Generates embedding for a given text."""
    client = get_client()
    if not client:
        # Return random normalized embedding for testing if no key
        vec = np.random.rand(1536)
        return (vec / np.linalg.norm(vec)).tolist()
    
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"⚠️ Error getting embedding: {e}")
        print("Falling back to random embedding for testing.")
        vec = np.random.rand(1536)
        return (vec / np.linalg.norm(vec)).tolist()

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
