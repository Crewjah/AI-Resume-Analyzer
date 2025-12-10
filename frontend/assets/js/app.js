// DOM elements
const form = document.getElementById('analyze-form');
const fileInput = document.getElementById('file');
const jobInput = document.getElementById('job_description');
const resultsPanel = document.getElementById('results');
const statusChip = document.getElementById('status-chip');
const submitBtn = document.getElementById('submit-btn');
const backendUrlLabel = document.getElementById('backend-url');

// API configuration - loaded from config.js
// Fallback: auto-detect from current window location if API_BASE not set
let API = window.API_BASE;
if (!API) {
  const protocol = window.location.protocol;
  const hostname = window.location.hostname;
  API = `${protocol}//${hostname}:5000`;
}

// Display backend URL
if (backendUrlLabel) {
  backendUrlLabel.textContent = API;
  console.log('API Base URL:', API);
}

function setStatus(text, tone = 'idle') {
  statusChip.textContent = text;
  statusChip.className = `status status--${tone}`;
}

function renderMetrics(data) {
  const jobMatch = data.job_analysis ? `${data.job_analysis.match_score}%` : 'N/A';
  return `
    <div class="metrics">
      <div class="metric"><div class="metric__label">ATS Score</div><div class="metric__value">${data.ats_score || 0}%</div></div>
      <div class="metric"><div class="metric__label">Skills</div><div class="metric__value">${data.skill_count || 0}</div></div>
      <div class="metric"><div class="metric__label">Job Match</div><div class="metric__value">${jobMatch}</div></div>
      <div class="metric"><div class="metric__label">Experience</div><div class="metric__value">${data.experience_years || 0} yrs</div></div>
      <div class="metric"><div class="metric__label">Words</div><div class="metric__value">${data.word_count || 0}</div></div>
    </div>
  `;
}

function renderSkills(skills) {
  if (!skills || Object.keys(skills).length === 0) return '';
  const groups = Object.entries(skills)
    .map(([cat, list]) => `<div class="pill pill--ghost">${cat}: ${list.join(', ')}</div>`)  
    .join('');
  return `<div class="section"><h3>Skills</h3><div class="pill-row">${groups}</div></div>`;
}

function renderKeywords(keywords) {
  if (!keywords || keywords.length === 0) return '';
  const chips = keywords.map(k => `<span class="chip">${k}</span>`).join('');
  return `<div class="section"><h3>Keywords</h3><div class="chip-row">${chips}</div></div>`;
}

function renderJobAnalysis(job) {
  if (!job) return '';
  const matched = job.matched_keywords?.map(k => `<span class="chip chip--success">${k}</span>`).join('') || '';
  const missing = job.missing_keywords?.map(k => `<span class="chip chip--warn">${k}</span>`).join('') || '';
  return `
    <div class="section">
      <h3>Job Match</h3>
      <div class="metric metric--inline">
        <div class="metric__label">Match Score</div>
        <div class="metric__value">${job.match_score || 0}%</div>
      </div>
      <div class="chip-group">
        <div><p class="muted">Matched</p>${matched || '<span class="muted">None</span>'}</div>
        <div><p class="muted">Missing</p>${missing || '<span class="muted">None</span>'}</div>
      </div>
    </div>
  `;
}

function renderRecommendations(recs) {
  if (!recs || recs.length === 0) return '';
  const items = recs.map(r => `<li>${r}</li>`).join('');
  return `<div class="section"><h3>Recommendations</h3><ul class="list">${items}</ul></div>`;
}

function renderResults(data) {
  const parts = [
    renderMetrics(data),
    renderSkills(data.skills),
    renderKeywords(data.keywords),
    renderJobAnalysis(data.job_analysis),
    renderRecommendations(data.recommendations),
  ].filter(Boolean);

  resultsPanel.innerHTML = parts.join('');
}

async function analyze(event) {
  event.preventDefault();
  
  // Validate file selection
  if (!fileInput.files || fileInput.files.length === 0) {
    setStatus('No file selected', 'error');
    resultsPanel.innerHTML = '<div class="alert alert--error">Please select a file to analyze.</div>';
    return;
  }

  const file = fileInput.files[0];
  const validExtensions = ['pdf', 'docx', 'txt'];
  const fileExt = file.name.split('.').pop().toLowerCase();
  
  if (!validExtensions.includes(fileExt)) {
    setStatus('Invalid file', 'error');
    resultsPanel.innerHTML = `<div class="alert alert--error">Only PDF, DOCX, and TXT files are supported. You uploaded: ${fileExt}</div>`;
    return;
  }

  // Prepare form data
  const formData = new FormData();
  formData.append('file', file);
  
  const jobDesc = jobInput.value.trim();
  if (jobDesc) {
    formData.append('job_description', jobDesc);
  }

  // Update UI
  setStatus('Analyzing…', 'info');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Analyzing…';

  try {
    // Make request to backend
    const analyzeUrl = `${API}/analyze`;
    console.log('Sending request to:', analyzeUrl);
    
    const response = await fetch(analyzeUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
      }
    });

    console.log('Response status:', response.status);

    // Try JSON first; if it fails, read text to surface HTML/error pages
    let data = null;
    try {
      data = await response.json();
    } catch (parseErr) {
      console.warn('Failed to parse JSON, falling back to text:', parseErr);
      const text = await response.text();
      console.warn('Raw response body:', text?.slice(0, 500));
      data = { error: text || 'Invalid response from server' };
    }

    if (!response.ok) {
      const errorMsg = data?.error || response.statusText || `HTTP ${response.status}`;
      console.error('Backend error:', errorMsg);
      setStatus('Failed', 'error');
      resultsPanel.innerHTML = `<div class="alert alert--error">${errorMsg}<br><small>Backend URL: ${API}</small></div>`;
      return;
    }

    // Success
    setStatus('Complete', 'success');
    renderResults(data);
    
  } catch (error) {
    console.error('Fetch error:', error);
    const errorMsg = error?.message || 'Failed to connect to server';
    setStatus('Network error', 'error');
    resultsPanel.innerHTML = `<div class="alert alert--error"><strong>Error:</strong> ${errorMsg}<br><small>Backend URL: ${API}</small></div>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Analyze';
  }
}

form.addEventListener('submit', analyze);

// Dropzone visual feedback
const dropzone = document.getElementById('dropzone');
['dragenter', 'dragover'].forEach(evt => dropzone.addEventListener(evt, e => {
  e.preventDefault();
  dropzone.classList.add('dropzone--active');
}));
['dragleave', 'drop'].forEach(evt => dropzone.addEventListener(evt, e => {
  e.preventDefault();
  dropzone.classList.remove('dropzone--active');
}));

dropzone.addEventListener('drop', e => {
  if (e.dataTransfer?.files?.length) {
    fileInput.files = e.dataTransfer.files;
  }
});
