import os
import sys

# Ensure project root is on sys.path so `src` package is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Start a local API server for tests if one isn't already available.
# This fixture runs the Flask `app` from `api/index.py` in a separate
# process for the duration of the test session and sets the
# `TEST_API_BASE` environment variable so tests use the running server.
import multiprocessing
import time
import requests

from typing import Generator


def _wait_for_health(url: str, timeout: float = 10.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{url}/health", timeout=1.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


def _run_app():
    # Import here to avoid side-effects at module import time
    from backend.app import app

    # Run Flask app without the reloader; debug=False prevents Werkzeug from
    # spawning extra processes which simplifies lifecycle management.
    app.run(host='127.0.0.1', port=5000, debug=False)


def pytest_configure(config):
    # Ensure tests use TEST_API_BASE env var
    base = os.environ.get('TEST_API_BASE', 'http://127.0.0.1:5000')
    os.environ['TEST_API_BASE'] = base


def pytest_sessionstart(session):
    # If server is already available, don't start another one
    base = os.environ.get('TEST_API_BASE', 'http://127.0.0.1:5000')
    try:
        r = requests.get(f"{base}/health", timeout=0.5)
        if r.status_code == 200:
            return
    except Exception:
        pass

    # Start the Flask app in a separate process
    proc = multiprocessing.Process(target=_run_app, daemon=True)
    proc.start()

    # Wait for the server to be healthy; if it doesn't come up, fail early
    if not _wait_for_health(base, timeout=10.0):
        proc.terminate()
        raise RuntimeError("Failed to start API server for tests (health check failed).")

    # Store process on the session for teardown
    session._api_process = proc


def pytest_sessionfinish(session, exitstatus):
    # Stop the server process if we started one
    proc = getattr(session, '_api_process', None)
    if proc is not None:
        proc.terminate()
        proc.join(timeout=5)
