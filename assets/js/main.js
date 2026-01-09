// AI Resume Analyzer - Enhanced Main JavaScript

// State management
const state = {
    currentPage: 'home',
    analysisResult: null,
    uploadedFiles: [],
    sidebarOpen: true
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Setup navigation
    setupNavigation();
    
    // Setup sidebar
    setupSidebar();
    
    // Setup file upload with drag and drop
    setupFileUpload();
    
    // Setup form submission
    setupFormSubmission();
    
    // Setup action buttons
    setupActionButtons();
    
    // Setup toggles and interactions
    setupInteractions();
    
    // Show initial page
    showPage('home');
}

// ===== Sidebar Management =====
function setupSidebar() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            state.sidebarOpen = sidebar.classList.contains('active');
        });
    }
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            state.sidebarOpen = sidebar.classList.contains('active');
        });
    }
    
    // Close sidebar on mobile when clicking a link
    const navLinks = sidebar.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 1024) {
                sidebar.classList.remove('active');
            }
        });
    });
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
    
    // Update page title
    const pageTitles = {
        'home': 'AI Resume Analyzer',
        'upload': 'Upload Resume',
        'dashboard': 'Analysis Dashboard',
        'job-matching': 'Job Matching',
        'ats-optimization': 'ATS Optimization',
        'reports': 'Reports & Export',
        'about': 'About'
    };
    
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
        pageTitle.textContent = pageTitles[pageName] || 'AI Resume Analyzer';
    }
    
    state.currentPage = pageName;
}

// ===== File Upload with Drag & Drop =====
function setupFileUpload() {
    const fileInput = document.getElementById('resume-file');
    const uploadZone = document.getElementById('upload-zone');
    const uploadArea = document.getElementById('file-upload-area');
    const filesContainer = document.getElementById('files-container');
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    
    if (!fileInput || !uploadZone) return;
    
    // Click to upload
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
    
    // Drag and drop events
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files);
    });
}

function handleFiles(files) {
    const filesArray = Array.from(files);
    const uploadZone = document.getElementById('upload-zone');
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    const filesContainer = document.getElementById('files-container');
    
    filesArray.forEach(file => {
        if (validateFile(file)) {
            state.uploadedFiles.push(file);
            addFileToList(file);
        }
    });
    
    if (state.uploadedFiles.length > 0) {
        uploadZone.classList.add('hidden');
        uploadedFilesList.classList.remove('hidden');
    }
}

function addFileToList(file) {
    const filesContainer = document.getElementById('files-container');
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
        <div class="file-item-info">
            <div class="file-item-icon">📄</div>
            <div class="file-item-details">
                <div class="file-item-name">${escapeHtml(file.name)}</div>
                <div class="file-item-size">${formatFileSize(file.size)}</div>
            </div>
        </div>
        <button type="button" class="file-item-remove" onclick="removeFile('${escapeHtml(file.name)}')">Remove</button>
    `;
    filesContainer.appendChild(fileItem);
}

function removeFile(fileName) {
    state.uploadedFiles = state.uploadedFiles.filter(f => f.name !== fileName);
    
    const filesContainer = document.getElementById('files-container');
    const uploadZone = document.getElementById('upload-zone');
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    
    // Remove from DOM
    const fileItems = filesContainer.querySelectorAll('.file-item');
    fileItems.forEach(item => {
        if (item.querySelector('.file-item-name').textContent === fileName) {
            item.remove();
        }
    });
    
    if (state.uploadedFiles.length === 0) {
        uploadZone.classList.remove('hidden');
        uploadedFilesList.classList.add('hidden');
        document.getElementById('resume-file').value = '';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

function validateFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
    
    if (file.size > maxSize) {
        showToast('File size must be less than 5MB', 'error');
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Please upload a PDF, TXT, or DOCX file', 'error');
        return false;
    }
    
    return true;
}

// ===== Interactions Setup =====
function setupInteractions() {
    // Job description toggle
    const jdToggle = document.getElementById('jd-toggle');
    const jobDescription = document.getElementById('job-description');
    
    if (jdToggle && jobDescription) {
        jdToggle.addEventListener('change', (e) => {
            if (e.target.checked) {
                jobDescription.classList.remove('hidden');
            } else {
                jobDescription.classList.add('hidden');
            }
        });
    }
    
    // Modal close handlers
    const modalOverlay = document.getElementById('modal-overlay');
    const modalClose = document.getElementById('modal-close');
    const modalCancel = document.getElementById('modal-cancel');
    
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }
    
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    if (modalCancel) {
        modalCancel.addEventListener('click', closeModal);
    }
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
    const jobDescription = document.getElementById('job-description').value;
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = analyzeBtn.querySelector('.btn-loader');
    
    if (state.uploadedFiles.length === 0) {
        showToast('Please select a resume file', 'error');
        return;
    }
    
    const file = state.uploadedFiles[0]; // Use first file for now
    
    // Show loading state
    analyzeBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    showToast('Analyzing your resume...', 'info');
    
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
            showToast('Analysis complete!', 'success');
            setTimeout(() => {
                showPage('dashboard');
            }, 1000);
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Analysis error:', error);
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

// ===== Toast Notifications =====
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '✓',
        error: '✗',
        warning: '⚠',
        info: 'ℹ'
    };
    
    const titles = {
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        info: 'Information'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <div class="toast-content">
            <div class="toast-title">${titles[type] || titles.info}</div>
            <div class="toast-message">${escapeHtml(message)}</div>
        </div>
        <button class="toast-close">&times;</button>
    `;
    
    toastContainer.appendChild(toast);
    
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.remove();
    });
    
    if (duration > 0) {
        setTimeout(() => {
            toast.remove();
        }, duration);
    }
}

// ===== Modal Functions =====
function showModal(title, body, confirmText = 'Confirm', onConfirm = null) {
    const overlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const confirmBtn = document.getElementById('modal-confirm');
    
    modalTitle.textContent = title;
    modalBody.innerHTML = body;
    confirmBtn.textContent = confirmText;
    
    overlay.classList.remove('hidden');
    
    if (onConfirm) {
        confirmBtn.onclick = () => {
            onConfirm();
            closeModal();
        };
    }
}

function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.add('hidden');
}

// ===== Display Results =====
function displayResults(data) {
    // Show results content, hide empty state
    document.getElementById('no-results').classList.add('hidden');
    document.getElementById('results-content').classList.remove('hidden');
    
    // Update summary cards
    updateSummaryCards(data);
    
    // Display scores
    displayScores(data.scores);
    
    // Display skills
    displaySkills(data.technical_skills, data.soft_skills);
    
    // Display recommendations
    displayRecommendations(data.recommendations);
    
    // Display additional info
    displayAdditionalInfo(data);
}

function updateSummaryCards(data) {
    const overallScore = data.scores.overall_score;
    const techSkills = data.technical_skills ? data.technical_skills.length : 0;
    const softSkills = data.soft_skills ? data.soft_skills.length : 0;
    const recommendations = data.recommendations ? data.recommendations.length : 0;
    
    const summaryOverall = document.getElementById('summary-overall');
    const summaryAts = document.getElementById('summary-ats');
    const summarySkills = document.getElementById('summary-skills');
    const summaryImprovements = document.getElementById('summary-improvements');
    
    if (summaryOverall) summaryOverall.textContent = `${overallScore}%`;
    if (summaryAts) summaryAts.textContent = data.scores.ats_compatibility >= 70 ? 'Yes' : 'No';
    if (summarySkills) summarySkills.textContent = techSkills + softSkills;
    if (summaryImprovements) summaryImprovements.textContent = recommendations;
}

function displayScores(scores) {
    const overallScore = scores.overall_score;
    
    // Update overall score with circular progress
    const scoreValue = document.getElementById('overall-score-value');
    const scoreLabel = document.getElementById('overall-score-label');
    const circleProgress = document.getElementById('overall-circle-progress');
    
    if (scoreValue) scoreValue.textContent = overallScore;
    
    // Set label based on score
    let label, color;
    if (overallScore >= 80) {
        label = 'Excellent';
        color = '#10B981';
    } else if (overallScore >= 60) {
        label = 'Good';
        color = '#2563EB';
    } else if (overallScore >= 40) {
        label = 'Needs Improvement';
        color = '#F59E0B';
    } else {
        label = 'Needs Significant Work';
        color = '#EF4444';
    }
    
    if (scoreLabel) {
        scoreLabel.textContent = label;
        scoreLabel.style.color = color;
    }
    
    // Animate circular progress
    if (circleProgress) {
        const circumference = 2 * Math.PI * 80;
        const offset = circumference - (overallScore / 100) * circumference;
        circleProgress.style.strokeDashoffset = offset;
        circleProgress.style.stroke = color;
    }
    
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
    const downloadBtn = document.getElementById('download-report');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadReport);
    }
    
    // Analyze another
    const analyzeAnotherBtn = document.getElementById('analyze-another');
    if (analyzeAnotherBtn) {
        analyzeAnotherBtn.addEventListener('click', () => {
            state.uploadedFiles = [];
            const filesContainer = document.getElementById('files-container');
            if (filesContainer) filesContainer.innerHTML = '';
            document.getElementById('job-description').value = '';
            showPage('upload');
        });
    }
}

// ===== Expandable Cards =====
function toggleExpand(button) {
    const card = button.closest('.score-card');
    const details = card.querySelector('.score-details');
    const icon = button.querySelector('.expand-icon');
    
    if (details.classList.contains('hidden')) {
        details.classList.remove('hidden');
        button.classList.add('active');
    } else {
        details.classList.add('hidden');
        button.classList.remove('active');
    }
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

// Make functions globally available
window.showPage = showPage;
window.removeFile = removeFile;
window.toggleExpand = toggleExpand;
window.showModal = showModal;
window.closeModal = closeModal;
window.showToast = showToast;
window.toggleExpandable = toggleExpandable;
window.simulateProgress = simulateProgress;

// ===== Enhanced Interactive Features =====

// Toggle expandable sections
function toggleExpandable(element) {
    const section = element.closest('.expandable-section');
    if (section) {
        section.classList.toggle('expanded');
    }
}

// Upload progress simulation
function simulateProgress(duration = 2000) {
    const progressWrapper = document.getElementById('upload-progress-wrapper');
    const progressBar = document.getElementById('upload-progress-bar');
    const progressPercentage = document.querySelector('.progress-percentage');
    
    if (!progressWrapper || progressBar.style.width === '100%') {
        return;
    }
    
    progressWrapper.classList.remove('hidden');
    progressBar.style.width = '0%';
    
    const steps = 100;
    const interval = duration / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += Math.random() * 30;
        if (current > 100) current = 100;
        
        progressBar.style.width = current + '%';
        progressPercentage.textContent = Math.round(current) + '%';
        
        if (current >= 100) {
            clearInterval(timer);
            setTimeout(() => {
                progressBar.style.width = '100%';
                progressPercentage.textContent = '100%';
            }, 200);
        }
    }, interval);
}

// Enhanced file validation with preview
function validateFileWithPreview(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const validTypes = ['application/pdf', 'text/plain', 'application/msword', 
                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (file.size > maxSize) {
        showToast(`File ${file.name} exceeds 5MB limit`, 'error');
        return false;
    }
    
    if (!validTypes.includes(file.type)) {
        showToast(`File format not supported for ${file.name}`, 'error');
        return false;
    }
    
    return true;
}

// Create file preview element
function createFilePreview(file) {
    const preview = document.createElement('div');
    preview.className = 'file-preview';
    
    // Get file type icon
    let fileTypeIcon = '?';
    if (file.type.includes('pdf')) fileTypeIcon = 'PDF';
    else if (file.type.includes('word')) fileTypeIcon = 'DOC';
    else if (file.type.includes('text')) fileTypeIcon = 'TXT';
    
    const lastModified = new Date(file.lastModified).toLocaleDateString();
    
    preview.innerHTML = `
        <div class="file-preview-thumbnail">${fileTypeIcon}</div>
        <div class="file-preview-info">
            <div class="file-preview-name">${escapeHtml(file.name)}</div>
            <div class="file-preview-meta">${formatFileSize(file.size)} • Modified: ${lastModified}</div>
        </div>
    `;
    
    return preview;
}

// Enhanced score display with animation
function displayScoresEnhanced(data) {
    if (!data) return;
    
    // Create detailed score breakdown
    const scoreBreakdown = {
        'Content Quality': data.content_quality_score || 0,
        'ATS Compatibility': data.ats_score || 0,
        'Keyword Optimization': data.keyword_score || 0,
        'Structure Analysis': data.structure_score || 0
    };
    
    const resultsContent = document.getElementById('results-content');
    if (!resultsContent) return;
    
    // Create breakdowndetailed display
    let breakdownHTML = `
        <div class="score-card-detailed">
            <div class="score-card-header">
                <h3 class="score-card-title">Score Breakdown</h3>
            </div>
            <div class="score-breakdown">
    `;
    
    for (const [label, value] of Object.entries(scoreBreakdown)) {
        const statusClass = value >= 70 ? 'status-good' : value >= 50 ? 'status-warning' : 'status-error';
        breakdownHTML += `
            <div class="breakdown-item">
                <span class="breakdown-label">${label}</span>
                <span class="breakdown-value">
                    <span class="status-badge ${statusClass}">${Math.round(value)}%</span>
                </span>
            </div>
        `;
    }
    
    breakdownHTML += '</div></div>';
    
    // Insert before other results if not already present
    if (!resultsContent.querySelector('.score-card-detailed')) {
        resultsContent.insertAdjacentHTML('afterbegin', breakdownHTML);
    }
}

// Create skill comparison cards
function createSkillComparison(resumeSkills, jobSkills) {
    const comparison = document.createElement('div');
    comparison.className = 'comparison-container';
    
    const matchedSkills = resumeSkills.filter(skill => 
        jobSkills.some(jskill => jskill.toLowerCase() === skill.toLowerCase())
    );
    
    const missingSkills = jobSkills.filter(skill =>
        !resumeSkills.some(rskill => rskill.toLowerCase() === skill.toLowerCase())
    );
    
    comparison.innerHTML = `
        <div class="comparison-column">
            <h3>Your Skills (${matchedSkills.length})</h3>
            <div class="skills-container">
                ${matchedSkills.map(skill => `<span class="skill-tag technical">${escapeHtml(skill)}</span>`).join('')}
            </div>
        </div>
        <div class="comparison-column">
            <h3>Missing Skills (${missingSkills.length})</h3>
            <div class="skills-container">
                ${missingSkills.map(skill => `<span class="skill-tag missing">${escapeHtml(skill)}</span>`).join('')}
            </div>
        </div>
    `;
    
    return comparison;
}

// Modal helper functions
function showModalAdvanced(title, content, options = {}) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay active';
    modal.id = 'dynamic-modal';
    
    const modalContent = `
        <div class="modal">
            <div class="modal-header">
                <h2>${escapeHtml(title)}</h2>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
        </div>
    `;
    
    modal.innerHTML = modalContent;
    document.body.appendChild(modal);
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Enhanced loading state
function showLoadingState(message = 'Processing your resume...') {
    const loader = document.createElement('div');
    loader.className = 'modal-overlay active';
    loader.id = 'loading-modal';
    loader.innerHTML = `
        <div class="modal" style="text-align: center; padding: 3rem;">
            <div class="loading-spinner" style="display: inline-block; margin-bottom: 1rem;"></div>
            <p style="color: var(--gray-600); font-size: 1rem;">${escapeHtml(message)}</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoadingState() {
    const loader = document.getElementById('loading-modal');
    if (loader) {
        loader.remove();
    }
}

// Enhanced tooltip initialization
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(elem => {
        elem.classList.add('tooltip-container');
        const tooltipText = elem.getAttribute('data-tooltip');
        const tooltip = document.createElement('span');
        tooltip.className = 'tooltip-text';
        tooltip.textContent = tooltipText;
        elem.appendChild(tooltip);
    });
}

// Create expandable sections
function createExpandableSection(title, content, isExpanded = false) {
    const section = document.createElement('div');
    section.className = `expandable-section ${isExpanded ? 'expanded' : ''}`;
    
    section.innerHTML = `
        <div class="expandable-header" onclick="toggleExpandable(this)">
            <h3>${escapeHtml(title)}</h3>
            <span class="expand-icon">▼</span>
        </div>
        <div class="expandable-content">
            ${content}
        </div>
    `;
    
    return section;
}

// Export to JSON
function exportToJSON(data) {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume-analysis.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Analysis exported as JSON', 'success');
}

// Export to CSV
function exportToCSV(data) {
    let csv = 'Metric,Score\n';
    csv += `Overall Score,${data.overall_score || 0}\n`;
    csv += `Content Quality,${data.content_quality_score || 0}\n`;
    csv += `ATS Score,${data.ats_score || 0}\n`;
    csv += `Keyword Optimization,${data.keyword_score || 0}\n`;
    csv += `Structure Score,${data.structure_score || 0}\n`;
    
    if (data.technical_skills) {
        csv += `\nTechnical Skills\n`;
        data.technical_skills.forEach(skill => {
            csv += `,"${escapeHtml(skill)}"\n`;
        });
    }
    
    if (data.soft_skills) {
        csv += `\nSoft Skills\n`;
        data.soft_skills.forEach(skill => {
            csv += `,"${escapeHtml(skill)}"\n`;
        });
    }
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume-analysis.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Analysis exported as CSV', 'success');
}

// Initialize tooltips on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeTooltips();
    setupJobMatching();
});

// ===== Job Matching Setup =====
const sampleJobDescriptions = {
    frontend: `Senior Frontend Developer

Location: San Francisco, CA
Salary: $150,000 - $200,000

About the Role:
We're looking for a Senior Frontend Developer to lead our web application development. You'll work with React, TypeScript, and modern web technologies.

Key Responsibilities:
- Design and develop user-facing features
- Collaborate with UX/UI designers and backend engineers
- Optimize application performance
- Mentor junior developers
- Participate in code reviews

Required Skills:
- 5+ years of frontend development experience
- Expert-level JavaScript/TypeScript
- React and state management (Redux/Context)
- HTML5 and CSS3
- Git and version control
- REST API integration
- Jest/React Testing Library

Nice to Have:
- GraphQL experience
- NextJS knowledge
- Performance optimization skills
- AWS or cloud experience
- Agile/Scrum experience`,

    backend: `Backend Engineer - Node.js

About the Role:
Join our team as a Backend Engineer and help build scalable server-side applications using Node.js and modern JavaScript.

Key Requirements:
- 3+ years of backend development experience
- Strong Node.js expertise
- Express.js or similar framework
- MongoDB and relational databases (PostgreSQL)
- RESTful API design
- Authentication and security
- Docker and containerization
- API testing and debugging

Responsibilities:
- Develop robust server-side applications
- Design database schemas
- Implement security best practices
- Write clean, maintainable code
- Conduct code reviews

Nice to Have:
- GraphQL experience
- Microservices architecture
- CI/CD pipelines
- AWS Lambda experience
- Performance optimization`,

    fullstack: `Full Stack Developer

About the Position:
We need a Full Stack Developer to build and maintain web applications using React and Node.js.

Requirements:
- 4+ years of full stack experience
- React and modern JavaScript
- Node.js backend development
- Database design (SQL and NoSQL)
- HTML5 and CSS3
- Version control (Git)
- REST API development
- Problem-solving skills

Responsibilities:
- Develop front-end features
- Build server-side APIs
- Design database schemas
- Optimize application performance
- Collaborate with product team

Bonus Skills:
- TypeScript
- Docker
- AWS services
- Testing frameworks
- DevOps practices`,

    devops: `DevOps Engineer

About the Role:
Lead our infrastructure and deployment initiatives as a DevOps Engineer with strong cloud experience.

Requirements:
- 3+ years DevOps experience
- AWS or Azure expertise
- Docker and Kubernetes
- CI/CD pipelines (Jenkins, GitLab CI)
- Infrastructure as Code (Terraform)
- Linux system administration
- Scripting (Python, Bash)
- Monitoring and logging tools

Responsibilities:
- Design and maintain infrastructure
- Implement deployment pipelines
- Monitor system performance
- Ensure security and compliance
- Automate operational tasks

Desired Skills:
- Kubernetes orchestration
- Prometheus/ELK stack
- Terraform experience
- Database administration
- Disaster recovery`,

    datascience: `Data Science Engineer

About the Position:
Build machine learning models and data pipelines as a Data Science Engineer.

Requirements:
- 3+ years data science experience
- Python expertise
- Machine learning frameworks (TensorFlow, scikit-learn)
- SQL and database querying
- Statistical analysis
- Data visualization (Matplotlib, Seaborn)
- Git and version control
- Big data tools (Spark, Hadoop)

Responsibilities:
- Develop predictive models
- Create data pipelines
- Perform exploratory data analysis
- Optimize model performance
- Collaborate with engineers

Nice to Have:
- Deep learning experience
- NLP skills
- Computer vision
- A/B testing knowledge
- Cloud platforms (AWS, GCP)`
};

function setupJobMatching() {
    const sampleJobsSelect = document.getElementById('sample-jobs');
    const jobDescInput = document.getElementById('job-desc-input');
    const clearJobBtn = document.getElementById('clear-job-btn');
    const matchBtn = document.getElementById('match-btn');
    const industrySelect = document.getElementById('industry-select');
    
    // Load sample job descriptions
    if (sampleJobsSelect) {
        sampleJobsSelect.addEventListener('change', (e) => {
            if (e.target.value) {
                jobDescInput.value = sampleJobDescriptions[e.target.value];
                showToast('Sample job description loaded', 'info');
            }
        });
    }
    
    // Clear button
    if (clearJobBtn) {
        clearJobBtn.addEventListener('click', () => {
            jobDescInput.value = '';
            if (sampleJobsSelect) sampleJobsSelect.value = '';
            document.getElementById('matching-results').classList.add('hidden');
            showToast('Job description cleared', 'info');
        });
    }
    
    // Match button
    if (matchBtn) {
        matchBtn.addEventListener('click', analyzeJobMatch);
    }
    
    // Industry-specific tips
    if (industrySelect) {
        industrySelect.addEventListener('change', (e) => {
            displayIndustryTips(e.target.value);
        });
    }
}

function analyzeJobMatch() {
    const jobDescInput = document.getElementById('job-desc-input');
    const matchResults = document.getElementById('matching-results');
    
    if (!jobDescInput.value.trim()) {
        showToast('Please enter or select a job description', 'error');
        return;
    }
    
    if (!state.analysisResult) {
        showToast('Please analyze your resume first', 'error');
        showPage('upload');
        return;
    }
    
    // Show loading
    showLoadingState('Analyzing job match...');
    
    // Simulate analysis delay
    setTimeout(() => {
        hideLoadingState();
        
        // Extract keywords from job description
        const jobKeywords = extractKeywords(jobDescInput.value);
        const resumeKeywords = extractKeywords(
            state.analysisResult.technical_skills?.join(' ') + ' ' +
            state.analysisResult.soft_skills?.join(' ')
        );
        
        // Calculate match percentage
        const matchPercentage = calculateMatchPercentage(jobKeywords, resumeKeywords);
        
        // Display results
        displayJobMatchResults(matchPercentage, jobKeywords, resumeKeywords);
        matchResults.classList.remove('hidden');
        
        showToast('Job match analysis complete!', 'success');
    }, 1500);
}

function extractKeywords(text) {
    if (!text) return [];
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    // Filter out common words
    const commonWords = new Set(['the', 'and', 'or', 'is', 'are', 'was', 'be', 'have', 'has', 'do', 'does', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'you', 'your', 'this', 'that', 'it', 'a', 'an']);
    return [...new Set(words.filter(w => w.length > 2 && !commonWords.has(w)))];
}

function calculateMatchPercentage(jobKeywords, resumeKeywords) {
    if (jobKeywords.length === 0) return 0;
    const matches = jobKeywords.filter(k => 
        resumeKeywords.some(r => r.includes(k) || k.includes(r))
    );
    return Math.round((matches.length / jobKeywords.length) * 100);
}

function displayJobMatchResults(percentage, jobKeywords, resumeKeywords) {
    const compatibilityValue = document.getElementById('compatibility-value');
    const compatibilityFill = document.getElementById('compatibility-fill');
    const compatibilityLabel = document.getElementById('compatibility-label');
    
    // Update compatibility meter
    compatibilityValue.textContent = percentage + '%';
    compatibilityFill.style.width = percentage + '%';
    
    // Update label
    if (percentage >= 80) {
        compatibilityLabel.textContent = 'Excellent Match!';
        compatibilityLabel.style.color = 'var(--success-green)';
    } else if (percentage >= 60) {
        compatibilityLabel.textContent = 'Good Match';
        compatibilityLabel.style.color = 'var(--warning-amber)';
    } else if (percentage >= 40) {
        compatibilityLabel.textContent = 'Fair Match';
        compatibilityLabel.style.color = 'var(--warning-amber)';
    } else {
        compatibilityLabel.textContent = 'Low Match';
        compatibilityLabel.style.color = 'var(--error-red)';
    }
    
    // Update skills comparison
    const resumeSkillsDiv = document.getElementById('resume-skills');
    const jobSkillsDiv = document.getElementById('job-skills');
    
    if (resumeSkillsDiv && jobSkillsDiv) {
        resumeSkillsDiv.innerHTML = '<div class="skills-list-compact">' + 
            resumeKeywords.slice(0, 10).map(s => `<span class="skill-tag">${escapeHtml(s)}</span>`).join('') + 
            '</div>';
        
        jobSkillsDiv.innerHTML = '<div class="skills-list-compact">' + 
            jobKeywords.slice(0, 10).map(s => `<span class="skill-tag">${escapeHtml(s)}</span>`).join('') + 
            '</div>';
    }
    
    // Display missing skills
    const missingSkills = jobKeywords.filter(k => 
        !resumeKeywords.some(r => r.includes(k) || k.includes(r))
    );
    
    const missingSkillsList = document.getElementById('missing-skills-list');
    if (missingSkillsList) {
        missingSkillsList.innerHTML = missingSkills.slice(0, 8).map(s => 
            `<span class="skill-tag missing">${escapeHtml(s)}</span>`
        ).join('');
    }
    
    // Display suggestions
    const matchSuggestions = document.getElementById('match-suggestions');
    if (matchSuggestions) {
        const suggestions = [
            `Add keywords: ${missingSkills.slice(0, 5).join(', ')}`,
            'Highlight relevant experience that matches job requirements',
            'Add a professional summary targeting this position',
            'Update your skills section with job-specific keywords'
        ];
        
        matchSuggestions.innerHTML = suggestions.map(s => 
            `<li>${escapeHtml(s)}</li>`
        ).join('');
    }
}

// Initialize ATS analysis
function initializeATSAnalysis() {
    if (state.analysisResult) {
        analyzeATSCompatibility(state.analysisResult);
    }
}

// ATS Compatibility Analysis
function analyzeATSCompatibility(data) {
    const atsMainScore = document.getElementById('ats-main-score');
    const atsStatus = document.getElementById('ats-status');
    const keywordDensity = document.getElementById('keyword-density');
    const industryKeywords = document.getElementById('industry-keywords');
    const atsActionVerbs = document.getElementById('ats-action-verbs');
    const keywordCloud = document.getElementById('keyword-cloud');
    
    if (!data) return;
    
    // Calculate ATS score based on multiple factors
    let atsScore = 0;
    let checks = [];
    
    // Factor 1: Keyword optimization (30%)
    const keywordScore = data.keyword_score || 0;
    atsScore += keywordScore * 0.3;
    if (keywordScore >= 70) checks.push(true); else checks.push(false);
    
    // Factor 2: Content quality (25%)
    const contentScore = data.content_quality_score || 0;
    atsScore += contentScore * 0.25;
    if (contentScore >= 70) checks.push(true); else checks.push(false);
    
    // Factor 3: Structure (20%)
    const structureScore = data.structure_score || 0;
    atsScore += structureScore * 0.2;
    if (structureScore >= 70) checks.push(true); else checks.push(false);
    
    // Factor 4: Skills presence (25%)
    const skillsCount = (data.technical_skills?.length || 0) + (data.soft_skills?.length || 0);
    const skillsScore = Math.min(100, (skillsCount / 20) * 100);
    atsScore += skillsScore * 0.25;
    if (skillsCount >= 10) checks.push(true); else checks.push(false);
    
    // Update ATS display
    if (atsMainScore) atsMainScore.textContent = Math.round(atsScore);
    if (keywordDensity) keywordDensity.textContent = Math.round(keywordScore) + '%';
    if (industryKeywords) industryKeywords.textContent = data.technical_skills?.length || 0;
    if (atsActionVerbs) atsActionVerbs.textContent = data.action_verbs_count || 0;
    
    // Update status
    if (atsStatus) {
        if (atsScore >= 80) {
            atsStatus.innerHTML = '<span class="status-icon">✓</span><span>Excellent ATS Compatibility!</span>';
            atsStatus.style.color = 'var(--success-green)';
        } else if (atsScore >= 60) {
            atsStatus.innerHTML = '<span class="status-icon">[!]</span><span>Good ATS Score - Minor improvements needed</span>';
            atsStatus.style.color = 'var(--warning-amber)';
        } else {
            atsStatus.innerHTML = '<span class="status-icon">✗</span><span>Consider ATS optimization recommendations</span>';
            atsStatus.style.color = 'var(--error-red)';
        }
    }
    
    // Update keyword cloud
    if (keywordCloud && data.technical_skills) {
        keywordCloud.innerHTML = data.technical_skills.slice(0, 15).map(skill => 
            `<span class="keyword-tag">${escapeHtml(skill)}</span>`
        ).join('');
    }
    
    // Update checklist
    const checkboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    checkboxes.forEach((checkbox, index) => {
        if (index < checks.length) {
            checkbox.checked = checks[index];
        }
    });
}

// Industry-specific tips
const industryTips = {
    tech: {
        title: 'Technology Industry Tips',
        tips: [
            'Highlight programming languages: Python, JavaScript, Java, C++',
            'Emphasize cloud platforms: AWS, Azure, Google Cloud',
            'Include DevOps tools: Docker, Kubernetes, Jenkins',
            'Mention frameworks: React, Node.js, Django, Spring',
            'Use keywords: API, database, SQL, REST, microservices',
            'Include certifications: AWS, Azure, Google Cloud, Linux'
        ]
    },
    finance: {
        title: 'Finance Industry Tips',
        tips: [
            'Highlight financial software: Excel, SAP, Oracle',
            'Emphasize compliance knowledge: AML, KYC, GDPR',
            'Include certifications: CFA, CPA, CFP, FRM',
            'Use keywords: Financial analysis, risk management, audit',
            'Mention banking systems: Bloomberg, FactSet, Trading systems',
            'Highlight experience with: Investment analysis, portfolio management'
        ]
    },
    healthcare: {
        title: 'Healthcare Industry Tips',
        tips: [
            'Highlight healthcare software: EHR, HIPAA compliance',
            'Include certifications: RN, MD, DPT, relevant licenses',
            'Use keywords: Patient care, clinical documentation, HIPAA',
            'Mention tools: Electronic Health Records (EHR), medical databases',
            'Emphasize: Compliance, quality assurance, patient safety',
            'Include experience with: Insurance, healthcare IT, medical devices'
        ]
    },
    marketing: {
        title: 'Marketing Industry Tips',
        tips: [
            'Highlight tools: Google Analytics, SEO, SEM, social media',
            'Include platforms: HubSpot, Salesforce, marketing automation',
            'Use keywords: ROI, conversion rate, customer acquisition',
            'Mention skills: Content marketing, brand management, campaign management',
            'Emphasize: Data analysis, market research, competitive analysis',
            'Include certifications: Google Analytics, Hootsuite, Hubspot'
        ]
    },
    engineering: {
        title: 'Engineering Industry Tips',
        tips: [
            'Highlight software: CAD, MATLAB, Simulink, AutoCAD',
            'Include certifications: PE, FE, Six Sigma, PMP',
            'Use keywords: Design, analysis, testing, quality assurance',
            'Mention methodologies: Agile, waterfall, continuous improvement',
            'Emphasize: Technical specifications, documentation, problem-solving',
            'Include experience with: Project management, team leadership'
        ]
    },
    education: {
        title: 'Education Industry Tips',
        tips: [
            'Highlight certifications: Teaching credentials, relevant degrees',
            'Include platforms: Canvas, Blackboard, Google Classroom',
            'Use keywords: Curriculum development, student assessment, instruction',
            'Mention skills: Lesson planning, classroom management, differentiation',
            'Emphasize: Student outcomes, professional development, collaboration',
            'Include experience with: Online learning, special education, STEAM'
        ]
    }
};

function displayIndustryTips(industry) {
    const industryTipsDiv = document.getElementById('industry-tips');
    if (!industryTipsDiv) return;
    
    if (!industry) {
        industryTipsDiv.innerHTML = '<p class="empty-message">Select an industry to see specific tips</p>';
        return;
    }
    
    const tips = industryTips[industry];
    if (!tips) return;
    
    let html = `<h4>${tips.title}</h4><ul class="tips-list">`;
    tips.tips.forEach(tip => {
        html += `<li>${escapeHtml(tip)}</li>`;
    });
    html += '</ul>';
    
    industryTipsDiv.innerHTML = html;
    showToast(`${tips.title} displayed`, 'info');
}

// ===== Report Generation & Export =====

function initializeReports() {
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    const exportJsonBtn = document.getElementById('export-json-btn');
    const exportCsvBtn = document.getElementById('export-csv-btn');
    const generateLinkBtn = document.getElementById('generate-link-btn');
    const copyLinkBtn = document.getElementById('copy-link-btn');
    const downloadChartsBtn = document.getElementById('download-charts-btn');
    
    if (downloadPdfBtn) downloadPdfBtn.addEventListener('click', () => downloadReport('pdf'));
    if (exportJsonBtn) exportJsonBtn.addEventListener('click', () => exportToJSON(state.analysisResult));
    if (exportCsvBtn) exportCsvBtn.addEventListener('click', () => exportToCSV(state.analysisResult));
    if (generateLinkBtn) generateLinkBtn.addEventListener('click', generateShareableLink);
    if (copyLinkBtn) copyLinkBtn.addEventListener('click', copyShareLink);
    if (downloadChartsBtn) downloadChartsBtn.addEventListener('click', downloadChartImages);
}

function generateComprehensiveReport(analysisData, reportType = 'detailed') {
    if (!analysisData) return '';
    
    let report = '═══════════════════════════════════════════════════════════\n';
    report += '                    RESUME ANALYSIS REPORT\n';
    report += '═══════════════════════════════════════════════════════════\n\n';
    
    // Report Date
    const date = new Date();
    report += `Generated: ${date.toLocaleString()}\n`;
    report += `Report Type: ${reportType === 'detailed' ? 'Detailed' : 'Summary'}\n\n`;
    
    // Overall Scores
    report += '───────────────────────────────────────────────────────────\n';
    report += 'OVERALL SCORES\n';
    report += '───────────────────────────────────────────────────────────\n';
    report += `Overall Score:           ${analysisData.overall_score || 0}%\n`;
    report += `Content Quality:         ${analysisData.content_quality_score || 0}%\n`;
    report += `ATS Compatibility:       ${analysisData.ats_score || 0}%\n`;
    report += `Keyword Optimization:    ${analysisData.keyword_score || 0}%\n`;
    report += `Structure Analysis:      ${analysisData.structure_score || 0}%\n\n`;
    
    if (reportType === 'detailed') {
        // Technical Skills
        if (analysisData.technical_skills && analysisData.technical_skills.length > 0) {
            report += '───────────────────────────────────────────────────────────\n';
            report += 'TECHNICAL SKILLS IDENTIFIED\n';
            report += '───────────────────────────────────────────────────────────\n';
            analysisData.technical_skills.forEach((skill, i) => {
                report += `${i + 1}. ${skill}\n`;
            });
            report += '\n';
        }
        
        // Soft Skills
        if (analysisData.soft_skills && analysisData.soft_skills.length > 0) {
            report += '───────────────────────────────────────────────────────────\n';
            report += 'SOFT SKILLS IDENTIFIED\n';
            report += '───────────────────────────────────────────────────────────\n';
            analysisData.soft_skills.forEach((skill, i) => {
                report += `${i + 1}. ${skill}\n`;
            });
            report += '\n';
        }
        
        // Recommendations
        if (analysisData.recommendations && analysisData.recommendations.length > 0) {
            report += '───────────────────────────────────────────────────────────\n';
            report += 'RECOMMENDATIONS FOR IMPROVEMENT\n';
            report += '───────────────────────────────────────────────────────────\n';
            analysisData.recommendations.forEach((rec, i) => {
                report += `${i + 1}. ${rec}\n`;
            });
            report += '\n';
        }
        
        // Statistics
        report += '───────────────────────────────────────────────────────────\n';
        report += 'RESUME STATISTICS\n';
        report += '───────────────────────────────────────────────────────────\n';
        report += `Total Word Count:        ${analysisData.word_count || 0} words\n`;
        report += `Action Verbs Found:      ${analysisData.action_verbs_count || 0}\n`;
        report += `Sections Detected:       ${analysisData.sections_detected ? analysisData.sections_detected.length : 0}\n`;
        report += `Skills Found:            ${(analysisData.technical_skills?.length || 0) + (analysisData.soft_skills?.length || 0)}\n\n`;
    }
    
    report += '═══════════════════════════════════════════════════════════\n';
    report += 'End of Report\n';
    report += '═══════════════════════════════════════════════════════════\n';
    
    return report;
}

function downloadReport(format = 'text') {
    if (!state.analysisResult) {
        showToast('Please analyze a resume first', 'error');
        return;
    }
    
    const report = generateComprehensiveReport(state.analysisResult, 'detailed');
    const filename = `resume-analysis-${new Date().getTime()}.${format === 'pdf' ? 'pdf' : 'txt'}`;
    
    const blob = new Blob([report], { type: format === 'pdf' ? 'application/pdf' : 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast(`Report downloaded as ${format.toUpperCase()}`, 'success');
}

function generateShareableLink() {
    if (!state.analysisResult) {
        showToast('Please analyze a resume first', 'error');
        return;
    }
    
    // Generate a mock shareable link (in production, this would create a unique URL on your server)
    const linkId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    const shareLink = `${window.location.origin}?report=${linkId}`;
    
    const shareLinkInput = document.getElementById('share-link-input');
    const shareLinkDisplay = document.getElementById('share-link-display');
    
    if (shareLinkInput && shareLinkDisplay) {
        shareLinkInput.value = shareLink;
        shareLinkDisplay.classList.remove('hidden');
        showToast('Shareable link generated!', 'success');
    }
}

function copyShareLink() {
    const shareLinkInput = document.getElementById('share-link-input');
    if (shareLinkInput) {
        shareLinkInput.select();
        document.execCommand('copy');
        showToast('Link copied to clipboard!', 'success');
    }
}

function downloadChartImages() {
    if (!state.analysisResult) {
        showToast('Please analyze a resume first', 'error');
        return;
    }
    
    // This would require canvas-to-image conversion in production
    showToast('Chart export feature coming soon!', 'info');
}

// Setup reports on page load
function setupReportHandlers() {
    // This will be called after analysis is complete
    if (document.getElementById('download-pdf-btn')) {
        initializeReports();
    }
}

