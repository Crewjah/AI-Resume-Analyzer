/* global API_BASE */

const form = document.getElementById('analyze-form');
const fileInput = document.getElementById('file');
const jobInput = document.getElementById('job_description');
const resultsPanel = document.getElementById('results');
const statusChip = document.getElementById('status-chip');
const submitBtn = document.getElementById('submit-btn');
const backendUrlLabel = document.getElementById('backend-url');

const API = (typeof window !== 'undefined' && window.API_BASE) ? window.API_BASE : 'http://localhost:5000';
backendUrlLabel.textContent = API;

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
  if (!fileInput.files.length) {
    alert('Please select a file.');
    return;
  }

  const fd = new FormData();
  fd.append('file', fileInput.files[0]);
  if (jobInput.value.trim()) {
    fd.append('job_description', jobInput.value.trim());
  }

  setStatus('Analyzing…', 'info');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Analyzing…';

  try {
    const res = await fetch(`${API}/analyze`, {
      method: 'POST',
      body: fd,
    });

    const payload = await res.json();

    if (!res.ok || payload.error) {
      setStatus(payload.error || 'Failed', 'error');
      resultsPanel.innerHTML = `<div class="alert alert--error">${payload.error || 'Something went wrong.'}</div>`;
      return;
    }

    setStatus('Complete', 'success');
    renderResults(payload);
  } catch (err) {
    setStatus('Network error', 'error');
    resultsPanel.innerHTML = `<div class="alert alert--error">${err?.message || 'Request failed.'}</div>`;
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
