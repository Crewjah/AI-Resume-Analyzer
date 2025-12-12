AI Resume Analyzer — Release v2.0

Summary
- Canonicalized core logic under `src/` and removed conflicting top-level modules.
- Added robust resume validation and deterministic analysis outputs (no random/fake scoring).
- Clean, professional web UI with static assets under `api/static/` and a Flask API at `api/index.py`.
- Added unit and integration tests; updated CI to start the app before running tests.
- Dockerized app (Dockerfile + docker-compose.yml); image built and smoke-tested locally.
- Created and pushed git tag `v2.0`.

Highlights
- Analyzer: structured JSON output with `valid`, `word_count`, `skills`, `ats_score`, `experience_years`, and `recommendations`.
- API: `/analyze` (POST file) returns HTTP 400 for invalid/too-short content and 200 with structured analysis for valid resumes.
- Tests: `pytest` suite passes locally (7 passed, 1 warning).

Notes & Next Steps
- Recommended: publish Docker image to a registry (requires credentials).
- Recommended: Create GitHub Release (this file can be used as the release body).
- Optional: Enhance NLP with spaCy for better entity extraction and experience parsing.

Changelog
- See commits on `main` since the previous tag for detailed diffs.

Maintainers
- Repository owner: Crewjah
- Contact: via GitHub issues
