# AI Career Predictor API

This FastAPI service provides the career catalogue, quiz definitions, and ranked recommendations for the existing frontend.

## Run locally

```bash
cd AI-Career-Predictor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

The website and API are available at `http://localhost:8000`; interactive API docs are at `http://localhost:8000/docs`.

## Endpoints

- `GET /health` — health check
- `GET /questions` — questionnaire definitions and allowed choices
- `GET /careers` — public career summaries
- `GET /careers/{career_id}` — career details and sources
- `POST /recommend` — weighted top five matches

Example request:

```json
{
  "interests": ["technology", "problem solving"],
  "skills": ["curiosity", "analytical thinking"],
  "subjects": ["computer science", "mathematics"],
  "work": ["creating", "research"],
  "priorities": ["learning"]
}
```

Set `FRONTEND_ORIGINS` to a comma-separated list of exact allowed browser origins in deployment settings. The default allows the local frontend and `https://aicareerpredictor.vercel.app`. Answers are processed in memory and are not persisted.

When the frontend and API are hosted separately, set `window.APP_API_BASE_URL` in `frontend/config.js` to the API's HTTPS origin and set `FRONTEND_ORIGINS` on the API host to the frontend's origin. Do not put backend credentials in browser code. For the current Vercel project, keep the frontend Root Directory set to `frontend`; deploy the API as a separate Python service.
