// Set your API base URL here. For Vercel static hosting, point to your backend host
// e.g., https://your-backend.onrender.com
// If left undefined, it falls back to the same origin (useful for local dev with `backend` on 5000).
window.API_BASE = window.API_BASE || (typeof location !== 'undefined' ? `${location.origin.replace(/\/$/, '')}` : 'http://localhost:5000');
