# Endurance Data Platform

A private review of endurance and multisport training. See weekly training time by sport and open a week to inspect the activities behind the totals. The demo is synthetic. Strava is the planned live source.

## Run locally

With Docker Desktop running, build and run the image from the repository root:

```powershell
docker build -t endurance-data-platform .
docker run --rm -p 127.0.0.1:8000:8000 endurance-data-platform
```

Open [the FastAPI contract](http://127.0.0.1:8000/docs) to try `GET /api/demo/weeks`. The container currently returns a placeholder at `/`. During development, the Vite server can display the dashboard and proxy **Load demo** to FastAPI.

### Python development on Windows

With Python 3.12 available as `python`, run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements-test.txt
Set-Location backend
..\.venv\Scripts\python.exe -m pytest -xq
```

If a `.venv` already exists with the test dependencies, start at `Set-Location backend`. Use `-x` when debugging to stop at the first failure. Remove it to run the entire suite.

To work on the frontend separately, start `..\.venv\Scripts\python.exe -m uvicorn endurance.main:app --reload` from `backend`. In a second terminal, run `npm ci` and `npm run dev` from `frontend`. Vite forwards `/api` to FastAPI on port 8000.

## Next Python exercise

You own `backend/endurance/main.py` and `backend/endurance/training.py`. The next task is to serve the built Vite dashboard in place of the placeholder at `/`.

Start by locating `frontend/dist/index.html` relative to `main.py`. Look into FastAPI's `StaticFiles` and register any root mount after the API routes. Before running Docker, predict what should happen at `/`, `/api/health`, and `/api/demo/weeks` with and without the Vite build.

From `backend`, run the Python suite with the virtual environment:

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

The dashboard reads reports from FastAPI. The API passes synthetic summaries through the domain functions and serializes the resulting weeks and their activities. The demo slice has no database or live integration. The fixture validates software behavior and carries no claims about actual training.
