// API Configuration with easy overrides
// Precedence (highest to lowest):
// 1) URL query param: ?api=https://your-backend
// 2) localStorage:    localStorage.API_BASE
// 3) window.API_BASE: injected via script/env
// 4) Local dev:       http://127.0.0.1:5000
// 5) Production:      PROD_API_BASE (no port)

const PROD_API_BASE = 'https://www.crewjah.tech';

function getQueryApiOverride() {
  try {
    const params = new URLSearchParams(window.location.search);
    const api = params.get('api');
    return api || null;
  } catch (_) {
    return null;
  }
}

function getStoredApiOverride() {
  try {
    return localStorage.getItem('API_BASE');
  } catch (_) {
    return null;
  }
}

function getBackendUrl() {
  const queryApi = getQueryApiOverride();
  if (queryApi) {
    try { localStorage.setItem('API_BASE', queryApi); } catch (_) {}
    return queryApi;
  }

  const storedApi = getStoredApiOverride();
  if (storedApi) return storedApi;

  if (window.API_BASE && typeof window.API_BASE === 'string') {
    return window.API_BASE;
  }

  const host = window.location.hostname;

  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://127.0.0.1:5000';
  }

  return PROD_API_BASE || `${window.location.protocol}//${host}`;
}

window.API_BASE = getBackendUrl();
