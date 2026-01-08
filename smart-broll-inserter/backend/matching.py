import numpy as np
from typing import List, Dict, Any
from backend.utils import get_embedding, cosine_similarity

MIN_GAP_SECONDS = 3.0  # Minimum gap between insertions
MIN_START_OFFSET = 5.0 # Don't insert in first 5 seconds
MAX_INSERTIONS = 6
MIN_INSERTIONS = 3
DEFAULT_DURATION = 3.0 # Default B-roll duration if not specified

def match_brolls(transcript: List[Dict], brolls: List[Dict]) -> List[Dict]:
    """
    Matches B-rolls to transcript segments based on semantic similarity and heuristics.
    """
    
    # 1. Precompute embeddings for transcript segments
    segments_with_embeddings = []
    for seg in transcript:
        # We only care about segments that start after the offset
        if seg["start"] < MIN_START_OFFSET:
            continue
            
        emb = get_embedding(seg["text"])
        segments_with_embeddings.append({
            **seg,
            "embedding": emb
        })
        
    # 2. Score all possible pairs
    candidates = []
    
    for seg in segments_with_embeddings:
        for broll in brolls:
            score = cosine_similarity(seg["embedding"], broll["embedding"])
            
            # Boost score if keywords match (simple heuristic)
            # This is optional but helps if embeddings are fuzzy
            
            candidates.append({
                "segment": seg,
                "broll": broll,
                "score": score
            })
            
    # 3. Sort candidates by score (highest first)
    candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # 4. Select insertions (Greedy approach with constraints)
    timeline = []
    used_broll_ids = set()
    
    for cand in candidates:
        if len(timeline) >= MAX_INSERTIONS:
            break
            
        seg = cand["segment"]
        broll = cand["broll"]
        
        # Rule: Don't reuse same B-roll
        if broll["id"] in used_broll_ids:
            continue
            
        # Rule: Check overlap/spacing with existing insertions
        # Proposed insertion time: seg['start'] to seg['start'] + DEFAULT_DURATION
        start_time = seg["start"]
        end_time = start_time + DEFAULT_DURATION
        
        collision = False
        for item in timeline:
            existing_start = item["start_sec"]
            existing_end = existing_start + item["duration_sec"]
            
            # Check for overlap or being too close
            if not (end_time + MIN_GAP_SECONDS <= existing_start or start_time >= existing_end + MIN_GAP_SECONDS):
                collision = True
                break
        
        if not collision:
            timeline.append({
                "start_sec": start_time,
                "duration_sec": DEFAULT_DURATION,
                "broll_id": broll["id"],
                "confidence": round(float(cand["score"]), 2),
                "reason": f"Matched '{broll['description'][:30]}...' to '{seg['text'][:30]}...'"
            })
            used_broll_ids.add(broll["id"])
            
    # 5. Sort timeline by start time
    timeline.sort(key=lambda x: x["start_sec"])
    
    return timeline
