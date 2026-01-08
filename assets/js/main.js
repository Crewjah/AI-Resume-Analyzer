// AI Resume Analyzer - Main JavaScript

// State management
const state = {
    currentPage: 'upload',
    analysisResult: null,
    uploadedFile: null
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Setup navigation
    setupNavigation();
    
    // Setup file upload
    setupFileUpload();
    
    // Setup form submission
    setupFormSubmission();
    
    // Setup action buttons
    setupActionButtons();
    
    // Show initial page
    showPage('upload');
}

// ===== Navigation =====
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.dataset.page;
            showPage(page);
        });
    });
}

function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const targetPage = document.getElementById(`${pageName}-page`);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });
    
    state.currentPage = pageName;
}

// ===== File Upload =====
function setupFileUpload() {
    const fileInput = document.getElementById('resume-file');
    const fileNameDisplay = document.getElementById('file-name');
    const clearButton = document.getElementById('clear-file');
    const fileInputDisplay = document.querySelector('.file-input-display');
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file
            if (!validateFile(file)) {
                return;
            }
            
            state.uploadedFile = file;
            fileNameDisplay.textContent = file.name;
            fileInputDisplay.classList.add('has-file');
            clearButton.classList.remove('hidden');
        }
    });
    
    clearButton.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFile();
    });
}

function validateFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['application/pdf', 'text/plain'];
    
    if (file.size > maxSize) {
        showStatus('File size must be less than 5MB', 'error');
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        showStatus('Please upload a PDF or TXT file', 'error');
        return false;
    }
    
    return true;
}

function clearFile() {
    const fileInput = document.getElementById('resume-file');
    const fileNameDisplay = document.getElementById('file-name');
    const clearButton = document.getElementById('clear-file');
    const fileInputDisplay = document.querySelector('.file-input-display');
    
    fileInput.value = '';
    state.uploadedFile = null;
    fileNameDisplay.textContent = 'Choose a file (PDF or TXT, max 5MB)';
    fileInputDisplay.classList.remove('has-file');
    clearButton.classList.add('hidden');
}

// ===== Form Submission =====
function setupFormSubmission() {
    const form = document.getElementById('analyze-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await analyzeResume();
    });
}

async function analyzeResume() {
    const fileInput = document.getElementById('resume-file');
    const jobDescription = document.getElementById('job-description').value;
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    
    const file = fileInput.files[0];
    if (!file) {
        showStatus('Please select a resume file', 'error');
        return;
    }
    
    // Show loading state
    analyzeBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    showStatus('Analyzing your resume...', 'info');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        if (jobDescription.trim()) {
            formData.append('job_description', jobDescription.trim());
        }
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.ok && result.data) {
            state.analysisResult = result.data;
            displayResults(result.data);
            showStatus('Analysis complete!', 'success');
            setTimeout(() => {
                showPage('results');
            }, 1000);
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Analysis error:', error);
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('upload-status');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.classList.remove('hidden');
    
    // Auto-hide success/info messages
    if (type !== 'error') {
        setTimeout(() => {
            statusEl.classList.add('hidden');
        }, 3000);
    }
}

// ===== Display Results =====
function displayResults(data) {
    // Show results content, hide empty state
    document.getElementById('no-results').classList.add('hidden');
    document.getElementById('results-content').classList.remove('hidden');
    
    // Display scores
    displayScores(data.scores);
    
    // Display skills
    displaySkills(data.technical_skills, data.soft_skills);
    
    // Display recommendations
    displayRecommendations(data.recommendations);
    
    // Display additional info
    displayAdditionalInfo(data);
}

function displayScores(scores) {
    const overallScore = scores.overall_score;
    
    // Update overall score
    const scoreCircle = document.getElementById('overall-score-circle');
    const scoreValue = document.getElementById('overall-score-value');
    const scoreLabel = document.getElementById('overall-score-label');
    
    scoreValue.textContent = overallScore;
    
    // Set color and label based on score
    let category, label;
    if (overallScore >= 80) {
        category = 'excellent';
        label = 'Excellent';
    } else if (overallScore >= 60) {
        category = 'good';
        label = 'Good';
    } else if (overallScore >= 40) {
        category = 'fair';
        label = 'Needs Improvement';
    } else {
        category = 'poor';
        label = 'Needs Significant Work';
    }
    
    scoreCircle.className = `score-circle ${category}`;
    scoreLabel.textContent = label;
    scoreLabel.className = `score-label ${category}`;
    
    // Update individual scores
    updateScore('content', scores.content_quality);
    updateScore('keyword', scores.keyword_optimization);
    updateScore('ats', scores.ats_compatibility);
    updateScore('structure', scores.structure_score);
    updateScore('completeness', scores.completeness);
}

function updateScore(id, value) {
    const scoreEl = document.getElementById(`${id}-score`);
    const progressEl = document.getElementById(`${id}-progress`);
    
    scoreEl.textContent = `${value}%`;
    progressEl.style.width = `${value}%`;
    
    // Set color based on score
    let color;
    if (value >= 80) {
        color = '#10B981'; // success green
    } else if (value >= 60) {
        color = '#2563EB'; // primary blue
    } else if (value >= 40) {
        color = '#F59E0B'; // warning amber
    } else {
        color = '#EF4444'; // error red
    }
    
    progressEl.style.background = `linear-gradient(90deg, ${color} 0%, ${color}dd 100%)`;
}

function displaySkills(technicalSkills, softSkills) {
    const techContainer = document.getElementById('technical-skills');
    const softContainer = document.getElementById('soft-skills');
    
    // Display technical skills
    if (technicalSkills && technicalSkills.length > 0) {
        techContainer.innerHTML = technicalSkills
            .map(skill => `<span class="skill-badge">${escapeHtml(skill)}</span>`)
            .join('');
    } else {
        techContainer.innerHTML = '<p class="empty-message">No technical skills detected</p>';
    }
    
    // Display soft skills
    if (softSkills && softSkills.length > 0) {
        softContainer.innerHTML = softSkills
            .map(skill => `<span class="skill-badge soft">${escapeHtml(skill)}</span>`)
            .join('');
    } else {
        softContainer.innerHTML = '<p class="empty-message">No soft skills detected</p>';
    }
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations-list');
    
    if (recommendations && recommendations.length > 0) {
        container.innerHTML = recommendations
            .map(rec => `<div class="recommendation-item">${escapeHtml(rec)}</div>`)
            .join('');
    } else {
        container.innerHTML = '<p class="empty-message">No recommendations available</p>';
    }
}

function displayAdditionalInfo(data) {
    // Word count
    document.getElementById('word-count').textContent = data.word_count || 0;
    
    // Action verbs count
    document.getElementById('action-verbs-count').textContent = data.action_verbs_count || 0;
    
    // Sections count
    const sectionsCount = data.sections_detected ? data.sections_detected.length : 0;
    document.getElementById('sections-count').textContent = sectionsCount;
    
    // Skills count
    const techSkills = data.technical_skills ? data.technical_skills.length : 0;
    const softSkills = data.soft_skills ? data.soft_skills.length : 0;
    document.getElementById('skills-count').textContent = techSkills + softSkills;
}

// ===== Action Buttons =====
function setupActionButtons() {
    // Download report
    document.getElementById('download-report').addEventListener('click', downloadReport);
    
    // Analyze another
    document.getElementById('analyze-another').addEventListener('click', () => {
        clearFile();
        document.getElementById('job-description').value = '';
        showPage('upload');
    });
}

function downloadReport() {
    if (!state.analysisResult) {
        alert('No analysis data available');
        return;
    }
    
    const data = state.analysisResult;
    const scores = data.scores;
    
    // Create text report
    let report = 'AI RESUME ANALYZER - ANALYSIS REPORT\n';
    report += '=====================================\n\n';
    
    report += 'OVERALL SCORE\n';
    report += `Overall: ${scores.overall_score}%\n\n`;
    
    report += 'SCORE BREAKDOWN\n';
    report += `Content Quality: ${scores.content_quality}%\n`;
    report += `Keyword Optimization: ${scores.keyword_optimization}%\n`;
    report += `ATS Compatibility: ${scores.ats_compatibility}%\n`;
    report += `Structure: ${scores.structure_score}%\n`;
    report += `Completeness: ${scores.completeness}%\n\n`;
    
    if (data.technical_skills && data.technical_skills.length > 0) {
        report += 'TECHNICAL SKILLS FOUND\n';
        report += data.technical_skills.join(', ') + '\n\n';
    }
    
    if (data.soft_skills && data.soft_skills.length > 0) {
        report += 'SOFT SKILLS FOUND\n';
        report += data.soft_skills.join(', ') + '\n\n';
    }
    
    if (data.recommendations && data.recommendations.length > 0) {
        report += 'RECOMMENDATIONS\n';
        data.recommendations.forEach((rec, i) => {
            report += `${i + 1}. ${rec}\n`;
        });
        report += '\n';
    }
    
    report += 'STATISTICS\n';
    report += `Word Count: ${data.word_count}\n`;
    report += `Action Verbs: ${data.action_verbs_count}\n`;
    report += `Sections Detected: ${data.sections_detected ? data.sections_detected.length : 0}\n`;
    
    // Download as text file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume-analysis-report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ===== Utility Functions =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make showPage globally available
window.showPage = showPage;
