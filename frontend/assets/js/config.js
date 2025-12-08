// API Configuration - Auto-detect backend URL
// Force IPv4 (127.0.0.1) to avoid IPv6 connection issues

function getBackendUrl() {
  // Get current window location
  const host = window.location.hostname;
  const protocol = window.location.protocol;
  
  // Force IPv4 for localhost to avoid IPv6 issues
  if (host === 'localhost') {
    return `${protocol}//127.0.0.1:5000`;
  }
  
  // If already an IP or domain, use it as-is
  return `${protocol}//${host}:5000`;
}

window.API_BASE = getBackendUrl();
