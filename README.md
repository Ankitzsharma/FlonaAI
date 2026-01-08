# Smart B-Roll Inserter

## Overview
The **Smart B-Roll Inserter** is an AI-powered system that automatically plans and inserts B-roll clips into an A-roll (talking-head) video. It uses **OpenAI Whisper** for transcription, **OpenAI Embeddings** for semantic understanding, and a custom heuristic engine to create a narrative-driven timeline.

## Quick Start (Windows)

1.  **Install Dependencies**:
    Double-click `install_dependencies.bat` to install all Python and Node.js requirements.

2.  **Run Backend**:
    Double-click `run_backend.bat`. This starts the API server at `http://localhost:8000`.

3.  **Run Frontend**:
    Double-click `run_frontend.bat`. This starts the UI at `http://localhost:5173`.

4.  **Use the App**:
    Open `http://localhost:5173` in your browser.

## ⚠️ Important Note on API Usage

This system supports AI-powered transcription and semantic matching via an external API.

**Fallback Mode:**  
If the API key is missing, invalid, or out of quota (for example, rate-limited errors), the system automatically switches to **Mock Mode**:
- Uses a pre-written mock transcript.
- Uses generated mock embeddings for matching.
- Ensures the full application flow completes without crashing.

This allows the application to remain functional and testable even without API access.

## Manual Setup

### Prerequisites
*   Python 3.8+
*   Node.js 16+
*   FFmpeg installed and available in system PATH.

### Backend Setup
1.  Navigate to the project root:
    ```bash
    cd smart-broll-inserter
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  Configure Environment Variables:
    *   Copy `.env.example` to `.env`.
    *   Add your OpenAI API Key to `.env`.

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## How to Run Manually

### Start Backend
From the project root (Important: Do not `cd backend`):
```bash
python -m backend.main
```
The API will start at `http://localhost:8000`.

### Start Frontend
From the `frontend` directory:
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`.

## Troubleshooting

*   **"An error occurred"**: Check the backend terminal window for detailed error logs.
*   **ImportError**: Make sure you run the backend using `python -m backend.main` from the `smart-broll-inserter` folder, not inside the `backend` folder.
*   **FFmpeg not found**: Ensure FFmpeg is installed and added to your System PATH.
