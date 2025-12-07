"""
Backwards-compatibility entrypoint. The canonical API now lives in `backend/app.py`.
This module simply re-exports the Flask `app` so existing imports and tests keep
working. Static assets/UI from the old version have been moved out; use the new
frontend under `frontend/`.
"""

from backend.app import app  # noqa: F401


if __name__ == "__main__":
    # Allow running directly for local debugging
    app.run(host="0.0.0.0", port=5000, debug=False)