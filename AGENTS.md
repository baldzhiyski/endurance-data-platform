# Endurance Data Platform

A private multisport training review. Athletes compare weekly and monthly training and inspect the activities behind each total. The public portfolio uses recordings and screenshots with labeled synthetic data.

## Status

- **Done:** public repository and local clone. The owner approved the first-slice split and chose Strava as the sole real activity source.
- **Now:** first slice, Load demo → weekly totals → session drill-down. The owner wrote the training domain and HTTP route drafts. On request, the agent corrected UTC conversion, sport aliases, Berlin week assignment, and the demo route's validation and frontend response fields. The dashboard root still returns a placeholder.
- **Next:** the owner mounts the built Vite dashboard after the API routes and checks both local setups, with and without a build. Verify the local Docker demo before closing the slice.
- **Written by me (owner):** the activity model and extra metrics; the original normalization and weekly aggregation; the expanded synthetic fixtures; the FastAPI app, health route, and initial demo route and serializer.

## How we work

Agree on the who-writes-what split before each vertical slice. The owner writes the core backend and makes domain and architecture decisions. The agent writes setup, fixtures, tests, all frontend code, Docker, CI and README instructions. The agreed split determines who writes backend glue. Use `TODO(me)` comments for owner code. Put contracts, typing suggestions, test pointers and debugging hints in the comments. Leave imports, type definitions and function definitions to the owner unless they ask for a stub. Help the owner read failures and debug. Offer a hint first, then pseudocode, then an example from a different problem. Full solutions require an explicit request. Once the owner has an attempt, review correctness, edge cases and idiomatic Python without rewriting their code. Ask for a prediction before important runs and one reasoning question in review. Work in 45–90 minute sessions, use GitHub issues for open work, and update Status when a slice finishes.

## Stack and decisions

- Python 3.12, FastAPI, pytest, React, TypeScript, Vite, Material UI, Docker and GitHub Actions. PostgreSQL is the intended durable store once there is app-owned state to persist. The first demo runs with in-memory fixtures.
- Share the normalization and reporting functions between synthetic demo data and the future Strava connector so demo and live calculations have the same semantics.
- Prefer date-bounded on-demand Strava reads initially to avoid retaining live activity history. Confirm API access, allowed use and retention before enabling a connector.
- Group activities by the Monday of their start date in the reporting timezone. The demo uses Europe/Berlin. Store timestamps as UTC and measurements in seconds and meters.
- Serve the built frontend and the API from one Docker image to keep the local launch simple.

## Layout and commands

- `backend/endurance/training.py`: domain types and owner rules. `demo_data.py`: synthetic fixtures. `main.py`: HTTP API.
- `backend/tests/`: Python domain and API checks. From `backend`, run `python -m pytest -q` in an environment with `requirements-test.txt` installed.
- `frontend/`: typed dashboard. From that folder, `npm ci` and `npm run build`.
- From the root, `docker build -t endurance-data-platform .` and `docker run --rm -p 127.0.0.1:8000:8000 endurance-data-platform`.

## Rules

Use `main` and logical commits after the slice works. Agent commits end with a `Co-Authored-By:` trailer. The owner commits their own code, or explicitly asks the agent to commit it without the trailer. Push only on request. Keep secrets and real activity data out of Git and showcases. No paid services, public app deployment, or Notion changes without authorization. Report measured results with environment and workload. Keep handoff and documentation to this file, `CLAUDE.md` and `README.md`.
