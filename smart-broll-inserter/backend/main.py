import os
import uuid
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load env vars
load_dotenv()

from backend.transcription import transcribe_video
from backend.broll_analysis import analyze_brolls
from backend.matching import match_brolls
from backend.video_render import render_video

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files for serving output video
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

class BrollInput(BaseModel):
    id: str
    metadata: str

@app.post("/generate-plan")
async def generate_plan(
    a_roll: UploadFile = File(...),
    b_rolls: List[UploadFile] = File(...),
    b_rolls_metadata: str = Form(...) # JSON string
):
    import json
    try:
        metadata_list = json.loads(b_rolls_metadata)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid B-roll metadata format")

    # Constraints Check
    if len(b_rolls) != 6:
         raise HTTPException(status_code=400, detail="Exactly 6 B-roll clips are required")

    # Save A-roll
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    a_roll_path = os.path.join(session_dir, "a_roll.mp4")
    with open(a_roll_path, "wb") as buffer:
        shutil.copyfileobj(a_roll.file, buffer)

    # Save B-rolls
    broll_paths = {}
    for i, broll_file in enumerate(b_rolls):
        broll_id = metadata_list[i]["id"]
        path = os.path.join(session_dir, f"{broll_id}.mp4")
        with open(path, "wb") as buffer:
            shutil.copyfileobj(broll_file.file, buffer)
        broll_paths[broll_id] = path

    # 1. Transcription
    try:
        transcript = transcribe_video(a_roll_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    # 2. B-roll Analysis
    try:
        brolls_data = analyze_brolls(metadata_list)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"B-roll Analysis failed: {str(e)}")

    # 3. Matching
    try:
        timeline = match_brolls(transcript, brolls_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Matching logic failed: {str(e)}")

    # Add file paths to timeline for rendering
    for item in timeline:
        item["file_path"] = broll_paths[item["broll_id"]]

    # 4. Render (Optional but high signal)
    output_video_name = f"final_{session_id}.mp4"
    output_video_path = os.path.join(OUTPUT_DIR, output_video_name)
    
    try:
        render_video(a_roll_path, brolls_data, timeline, output_video_path)
        video_url = f"/output/{output_video_name}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Rendering failed: {e}")
        # We don't fail the request if rendering fails, just return no video
        video_url = None

    # Save timeline to JSON file
    plan_path = os.path.join(OUTPUT_DIR, f"plan_{session_id}.json")
    plan_data = {
        "transcript": transcript,
        "insertions": timeline,
        "video_url": video_url
    }
    with open(plan_path, "w") as f:
        json.dump(plan_data, f, indent=2)

    return plan_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
