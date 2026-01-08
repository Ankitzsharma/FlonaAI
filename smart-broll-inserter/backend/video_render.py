import os
import subprocess
from typing import List, Dict, Any

def render_video(a_roll_path: str, b_rolls: List[Dict], timeline: List[Dict], output_path: str):
    """
    Renders the final video by overlaying B-rolls on the A-roll using FFmpeg.
    
    timeline items: {"start_sec": float, "duration_sec": float, "broll_id": str, "file_path": str}
    """
    if not timeline:
        # Just copy A-roll if no insertions
        subprocess.run(["ffmpeg", "-y", "-i", a_roll_path, "-c", "copy", output_path], check=True)
        return

    # Filter timeline to include file paths
    # We need to ensure we have the correct file path for each broll_id
    
    # Building a complex FFmpeg filter_complex string
    # We'll use a simpler approach: concat or multiple overlays
    # For a robust solution, we can use the overlay filter with enable='between(t,start,end)'
    
    # 1. Inputs: A-roll is index 0, B-rolls are 1 to N
    input_args = ["-i", a_roll_path]
    broll_map = {} # broll_id -> index
    
    current_index = 1
    for item in timeline:
        broll_id = item["broll_id"]
        if broll_id not in broll_map:
            broll_map[broll_id] = current_index
            input_args.extend(["-i", item["file_path"]])
            current_index += 1
            
    # 2. Filter complex
    # Scale all B-rolls to match A-roll dimensions (assuming 1080p for safety or same as A-roll)
    # We'll use [0:v] as the base
    
    filters = []
    last_label = "[0:v]"
    
    for i, item in enumerate(timeline):
        broll_idx = broll_map[item["broll_id"]]
        start = item["start_sec"]
        end = start + item["duration_sec"]
        
        # Label for the current B-roll after scaling
        scaled_label = f"[v_broll{i}]"
        # Label for the output of this overlay
        out_label = f"[v_out{i}]"
        
        # Scale B-roll to match A-roll (forcing same aspect ratio for simplicity in this version)
        filters.append(f"[{broll_idx}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2{scaled_label}")
        
        # Overlay B-roll on top of the current base
        filters.append(f"{last_label}{scaled_label}overlay=0:0:enable='between(t,{start},{end})'{out_label}")
        
        last_label = out_label

    filter_str = ";".join(filters)
    
    # 3. Execute command
    command = [
        ffmpeg_exe, "-y"
    ] + input_args + [

        "-filter_complex", filter_str,
        "-map", last_label,
        "-map", "0:a", # Keep original audio
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "copy",
        output_path
    ]
    
    print(f"Executing FFmpeg command: {' '.join(command)}")
    subprocess.run(command, check=True)
