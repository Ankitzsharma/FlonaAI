import os
import requests

ASSETS_DIR = "sample_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

assets = {
    "a_roll.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/a_roll.mp4",
    "broll_1.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_1.mp4",
    "broll_2.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_2.mp4",
    "broll_3.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_3.mp4",
    "broll_4.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_4.mp4",
    "broll_5.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_5.mp4",
    "broll_6.mp4": "https://fzuudapb1wvjxbrr.public.blob.vercel-storage.com/food_quality_ugc/broll_6.mp4",
}

def download_file(url, filename):
    path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(path):
        print(f"{filename} already exists.")
        return
    
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    for filename, url in assets.items():
        download_file(url, filename)
