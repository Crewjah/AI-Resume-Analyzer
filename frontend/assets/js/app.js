/**
 * AI Resume Analyzer - Main Application
 * Handles file upload, form submission, and result rendering
 */

// DOM Elements
const form = document.getElementById('analyzer-form');
const fileInput = document.getElementById('resume-file');
const jobInput = document.getElementById('job-description');
const dropzone = document.getElementById('dropzone');
const resultsContainer = document.getElementById('results-container');
const statusBadge = document.getElementById('status-badge');
const submitBtn = document.getElementById('submit-btn');
const apiUrlDisplay = document.getElementById('api-url');
const fileInfo = document.getElementById('file-info');

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    displayApiUrl();
    setupDropzone();
    form.addEventListener('submit', handleFormSubmit);
});

/**
 * Display API endpoint in UI
 */
function displayApiUrl() {
    if (apiUrlDisplay) {
        apiUrlDisplay.textContent = window.API_ENDPOINT || '/api/analyze';
        apiUrlDisplay.title = window.API_ENDPOINT || '/api/analyze';
    }
}

/**
 * Setup drag-and-drop functionality
 */
function setupDropzone() {
    ['dragenter', 'dragover'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.add('active');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.remove('active');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer?.files?.length) {
            fileInput.files = e.dataTransfer.files;
            updateFileInfo();
        }
    });

    fileInput.addEventListener('change', updateFileInfo);
}

/**
 * Update file info display
 */
function updateFileInfo() {
    if (fileInput.files && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        fileInfo.textContent = `✓ ${file.name} (${sizeMB} MB)`;
        fileInfo.classList.add('visible');
    } else {
        fileInfo.classList.remove('visible');
    }
}

/**
 * Set status badge
 */
function setStatus(text, type = 'ready') {
    statusBadge.textContent = text;
    statusBadge.className = `status-badge ${type}`;
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    // Validation
    if (!fileInput.files || fileInput.files.length === 0) {
        setStatus('No file selected', 'error');
        showError('Please select a resume file to analyze.');
        return;
    }

    const file = fileInput.files[0];
    const validExtensions = ['pdf', 'docx', 'txt'];
    const fileExt = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(fileExt)) {
        setStatus('Invalid file type', 'error');
        showError(`Invalid file type. Allowed: ${validExtensions.join(', ').toUpperCase()}`);
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        setStatus('File too large', 'error');
        showError('File size exceeds 10 MB limit.');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', file);

    const jobDesc = jobInput.value.trim();
    if (jobDesc) {
        formData.append('job_description', jobDesc);
    }

    // Submit
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing…';
    setStatus('Analyzing…', 'loading');

    try {
        console.log('📤 Sending request to:', window.API_ENDPOINT);
        console.log('📋 File:', file.name, '(' + (file.size / 1024).toFixed(2) + ' KB)');
        
        const response = await fetch(window.API_ENDPOINT, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            }
        });

        console.log('📥 Response status:', response.status);

        // Parse response
        let data;
        try {
            data = await response.json();
            console.log('✅ Response data:', data);
        } catch (parseErr) {
            console.error('❌ JSON parse error:', parseErr);
            const text = await response.text();
            console.error('❌ Raw response:', text?.slice(0, 500));
            throw new Error('Invalid response format from server. ' + (text ? text.slice(0, 100) : 'Empty response'));
        }

        // Handle errors
        if (!response.ok) {
            const errorMsg = data?.error || data?.message || `HTTP ${response.status}`;
            console.error('❌ API error:', errorMsg);
            setStatus('Analysis failed', 'error');
            showError(`Server error: ${errorMsg}`);
            return;
        }

        // Check for validation errors
        if (data.valid === false) {
            setStatus('Invalid resume', 'error');
            showError(`Resume validation failed: ${data.message}`);
            return;
        }

        // Success
        setStatus('Complete', 'success');
        renderResults(data);

    } catch (error) {
        console.error('❌ Request error:', error);
        setStatus('Connection error', 'error');
        
        // Provide helpful error message
        let errorMsg = error.message;
        if (error.message.includes('Failed to fetch')) {
            errorMsg = `Cannot connect to API at ${window.API_ENDPOINT}. Make sure the backend server is running on port 5000.`;
        }
        
        showError(errorMsg);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span class="btn-text">Analyze Resume</span><span class="btn-icon">→</span>';
    }
}

/**
 * Show error message
 */
function showError(message) {
    resultsContainer.innerHTML = `
        <div class="alert alert--error">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

/**
 * Render results
 */
function renderResults(data) {
    const html = `
        ${renderMetrics(data)}
        ${renderSkills(data.skills)}
        ${renderKeywords(data.keywords)}
        ${data.job_analysis ? renderJobAnalysis(data.job_analysis) : ''}
        ${renderRecommendations(data.recommendations)}
    `;

    resultsContainer.innerHTML = html;
}

/**
 * Render metrics grid
 */
function renderMetrics(data) {
    const jobMatch = data.job_analysis?.match_score ?? 'N/A';
    return `
        <div class="metrics">
            <div class="metric">
                <div class="metric__label">ATS Score</div>
                <div class="metric__value">${data.ats_score || 0}%</div>
            </div>
            <div class="metric">
                <div class="metric__label">Skills Found</div>
                <div class="metric__value">${data.skill_count || 0}</div>
            </div>
            <div class="metric">
                <div class="metric__label">Job Match</div>
                <div class="metric__value">${jobMatch}%</div>
            </div>
            <div class="metric">
                <div class="metric__label">Experience</div>
                <div class="metric__value">${data.experience_years || 0} yrs</div>
            </div>
            <div class="metric">
                <div class="metric__label">Word Count</div>
                <div class="metric__value">${data.word_count || 0}</div>
            </div>
        </div>
    `;
}

/**
 * Render skills section
 */
function renderSkills(skills) {
    if (!skills || Object.keys(skills).length === 0) return '';

    const skillsHtml = Object.entries(skills)
        .map(([category, skillList]) => {
            const skillTags = skillList
                .map(skill => `<span class="pill">${skill}</span>`)
                .join('');
            return `
                <div style="margin-bottom: 1.5rem;">
                    <h4 style="margin-bottom: 0.5rem;">${category}</h4>
                    <div class="pill-row">${skillTags}</div>
                </div>
            `;
        })
        .join('');

    return `
        <div class="section">
            <h3>Skills</h3>
            ${skillsHtml}
        </div>
    `;
}

/**
 * Render keywords section
 */
function renderKeywords(keywords) {
    if (!keywords || keywords.length === 0) return '';

    const keywordChips = keywords
        .map(k => `<span class="chip">${k}</span>`)
        .join('');

    return `
        <div class="section">
            <h3>Professional Keywords</h3>
            <div class="chip-row">${keywordChips}</div>
        </div>
    `;
}

/**
 * Render job analysis section
 */
function renderJobAnalysis(job) {
    if (!job) return '';

    const matchedChips = (job.matched_keywords || [])
        .map(k => `<span class="chip chip--success">${k}</span>`)
        .join('');

    const missingChips = (job.missing_keywords || [])
        .map(k => `<span class="chip chip--warn">${k}</span>`)
        .join('');

    return `
        <div class="section">
            <h3>Job Match Analysis</h3>
            <div class="metric">
                <div class="metric__label">Match Score</div>
                <div class="metric__value">${job.match_score || 0}%</div>
            </div>
            <div class="chip-group" style="margin-top: 1.5rem;">
                <div>
                    <p style="font-weight: 600; margin-bottom: 0.5rem;">Matched Keywords</p>
                    <div class="chip-row">${matchedChips || '<span class="muted">None found</span>'}</div>
                </div>
                <div>
                    <p style="font-weight: 600; margin-bottom: 0.5rem;">Missing Keywords</p>
                    <div class="chip-row">${missingChips || '<span class="muted">All matched!</span>'}</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Render recommendations section
 */
function renderRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) return '';

    const items = recommendations
        .map(r => `<li>${r}</li>`)
        .join('');

    return `
        <div class="section">
            <h3>Recommendations</h3>
            <ul class="list">${items}</ul>
        </div>
    `;
}


