// API Configuration
// Rules:
// 1) If window.API_BASE is already set (injected via env/script), use it.
// 2) If running locally, force IPv4 localhost:5000.
// 3) Otherwise, default to your production backend host (no custom port).

// Default production API endpoint (change if you deploy backend elsewhere)
const PROD_API_BASE = 'https://www.crewjah.tech';

function getBackendUrl() {
  // Respect an injected override if present
  if (window.API_BASE && typeof window.API_BASE === 'string') {
    return window.API_BASE;
  }

  const host = window.location.hostname;
  const protocol = window.location.protocol;

  // Local dev: avoid IPv6/localhost issues
  if (host === 'localhost' || host === '127.0.0.1') {
    return 'http://127.0.0.1:5000';
  }

  // Production default (no custom port)
  return PROD_API_BASE || `${protocol}//${host}`;
}

window.API_BASE = getBackendUrl();
