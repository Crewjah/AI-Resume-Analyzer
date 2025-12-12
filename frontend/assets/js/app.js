/**
 * ResumAI - Modern Resume Analyzer
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
const fileInfo = document.getElementById('file-info');

// State
let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    setupDropzone();
    form.addEventListener('submit', handleFormSubmit);
});

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

    dropzone.addEventListener('drop', handleDrop);
    dropzone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
}

/**
 * Handle dropped files
 */
function handleDrop(e) {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
}

/**
 * Handle file selection
 */
function handleFileSelect() {
    const file = fileInput.files[0];
    if (file) {
        selectedFile = file;
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
        
        if (!validTypes.includes(file.type)) {
            showFileError('Invalid file type. Please upload PDF, DOCX, or TXT.');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            showFileError('File size exceeds 10MB limit.');
            return;
        }

        showFileSuccess(file.name);
    }
}

/**
 * Show file selection success
 */
function showFileSuccess(filename) {
    fileInfo.classList.add('visible');
    fileInfo.innerHTML = `✓ ${filename} ready for analysis`;
    fileInfo.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    fileInfo.style.color = 'white';
}

/**
 * Show file selection error
 */
function showFileError(message) {
    fileInfo.classList.add('visible');
    fileInfo.innerHTML = `✗ ${message}`;
    fileInfo.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    fileInfo.style.color = 'white';
    selectedFile = null;
    fileInput.value = '';
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    if (!selectedFile) {
        updateStatus('error', 'Please select a resume file');
        return;
    }

    updateStatus('loading', 'Analyzing your resume...');
    submitBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const jobDesc = jobInput.value.trim();
        if (jobDesc) {
            formData.append('job_description', jobDesc);
        }

        const endpoint = window.API_ENDPOINT || 'http://127.0.0.1:5000/api/analyze';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            }
        });

        // Read the response text once and reuse it
        const responseText = await response.text();
        
        if (!response.ok) {
            console.error('API Error:', response.status, responseText);
            updateStatus('error', `Error: ${response.status}`);
            displayError(response.status, responseText);
            return;
        }

        // Parse the JSON from the response text
        const data = JSON.parse(responseText);
        
        console.log('Analysis Results:', data);
        updateStatus('success', 'Analysis complete');
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        updateStatus('error', 'Analysis failed');
        displayError('Network Error', error.message);
    } finally {
        submitBtn.disabled = false;
    }
}

/**
 * Update status indicator
 */
function updateStatus(type, message) {
    statusBadge.className = `status-indicator ${type}`;
    statusBadge.textContent = message;
}

/**
 * Display error message
 */
function displayError(title, message) {
    resultsContainer.innerHTML = `
        <div class="alert alert--error">
            <strong>${title}</strong>
            <p>${message}</p>
        </div>
    `;
}

/**
 * Display analysis results
 */
function displayResults(data) {
    if (!data || typeof data !== 'object') {
        displayError('Error', 'Invalid response format');
        return;
    }

    const {
        ats_score = 0,
        detected_skills = [],
        years_of_experience = 0,
        suggestions = [],
        matched_skills = [],
        missing_skills = []
    } = data;

    let html = '<div class="results-content">';

    // Metrics
    html += `
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">ATS Score</div>
                <div class="metric-value">${Math.round(ats_score)}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Skills Found</div>
                <div class="metric-value">${detected_skills.length}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Experience</div>
                <div class="metric-value">${years_of_experience}y</div>
            </div>
        </div>
    `;

    // Skills Section
    if (detected_skills && detected_skills.length > 0) {
        html += `
            <div class="section">
                <h3 class="section-title">
                    <span class="section-icon">🎯</span>
                    Detected Skills
                </h3>
                <div class="pill-row">
                    ${detected_skills.map(skill => `<span class="pill">${skill}</span>`).join('')}
                </div>
            </div>
        `;
    }

    // Matched Skills
    if (matched_skills && matched_skills.length > 0) {
        html += `
            <div class="section">
                <h3 class="section-title">
                    <span class="section-icon">✓</span>
                    Matched Skills
                </h3>
                <div class="chip-row">
                    ${matched_skills.map(skill => `<span class="chip chip--success">${skill}</span>`).join('')}
                </div>
            </div>
        `;
    }

    // Missing Skills
    if (missing_skills && missing_skills.length > 0) {
        html += `
            <div class="section">
                <h3 class="section-title">
                    <span class="section-icon">📌</span>
                    Missing Skills
                </h3>
                <div class="chip-row">
                    ${missing_skills.map(skill => `<span class="chip chip--warning">${skill}</span>`).join('')}
                </div>
            </div>
        `;
    }

    // Suggestions
    if (suggestions && suggestions.length > 0) {
        html += `
            <div class="section">
                <h3 class="section-title">
                    <span class="section-icon">💡</span>
                    Improvement Tips
                </h3>
                <ul class="recommendation-list">
                    ${suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    html += '</div>';
    resultsContainer.innerHTML = html;
}
