import os
from typing import List, Dict, Any
from backend.utils import get_client, get_embedding


def refine_description(metadata: str) -> str:
    """Refines the B-roll metadata using LLM to be more descriptive for matching."""
    client = get_client()
    if not client:
        return metadata # Fallback
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a video editor helper. You will be given a raw description of a B-roll clip. specific visual details, mood, and context. Output only the refined description."},
                {"role": "user", "content": f"Refine this B-roll description: {metadata}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error refining description: {e}")
        return metadata

def analyze_brolls(brolls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyzes B-roll clips.
    Input: List of {"id": str, "metadata": str, ...}
    Output: List of {"id": str, "description": str, "embedding": List[float], ...}
    """
    analyzed_brolls = []
    
    for broll in brolls:
        # Refine description (optional, maybe skip to save time/cost if metadata is already good)
        # The provided metadata is already quite good, but let's assume we use it as is or slightly refined.
        # For this assignment, I'll use the metadata as the description directly to be safe, 
        # or just simple pass-through if "refine" isn't strictly requested to change content.
        # The prompt says: "Generate or refine a textual description... Use provided metadata and/or LLM-based descriptions"
        
        description = broll.get("metadata", "")
        # description = refine_description(description) # Uncomment if we want LLM refinement
        
        embedding = get_embedding(description)
        
        analyzed_brolls.append({
            **broll,
            "description": description,
            "embedding": embedding
        })
        
    return analyzed_brolls
