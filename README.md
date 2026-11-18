# AI Career Predictor

A complete career exploration website with a browser frontend and a Python JSON API. Quiz answers are used to calculate matches and are not saved by the service. Saved careers stay in the browser.

## Open the website on Mac

1. Unzip this folder.
2. Double-click `run.command`.
3. Your browser opens at `http://127.0.0.1:8000`.

Keep the Terminal window open while using the site. Close that window to stop it. The local server uses Python's standard library, so it needs no package installation or account setup.

If macOS blocks the first launch, right-click `run.command`, choose **Open**, and confirm. Alternatively open Terminal in this folder and run:

```bash
python3 backend/server.py
```

Then open `http://127.0.0.1:8000`.

## What's included

- A responsive landing page, five-step questionnaire, recommendations, career details, saved careers, share, and download actions.
- API endpoints: `GET /health`, `GET /questions`, `GET /careers`, `GET /careers/{id}`, and `POST /recommend`.
- Server-side input validation and weighted, explainable recommendation scoring.
- An optional FastAPI adapter in `backend/app/main.py` for hosting on a Python web service. Install `backend/requirements.txt`, then run `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000` from this folder.

## Deploy the full app to Render

Create a Render **Web Service** from this repository's project root. Use:

- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

FastAPI serves the frontend and API from the same service, so the deployed app has one public URL and needs no separate API URL or CORS setup. The Vercel project remains an optional frontend-only deployment.

The current app has no database. Career data ships with the code, quiz answers are not retained, and saved careers use this browser's local storage.

The career catalogue is a starter set. The scores indicate similarity within this catalogue, not likelihood of career success or employment. Education and licensing information varies by location.
