document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    if (!uploadForm) return;

    uploadForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const fileInput = document.getElementById('resumeFile');
        const fileWarning = document.getElementById('fileWarning');
        const MIN_BYTES = 2048; // 2 KB heuristic minimum
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');

        if (!fileInput.files[0]) {
            alert('Please select a resume file to analyze');
            return;
        }

        // Client-side file-size check to avoid uploading very small/invalid files
        const file = fileInput.files[0];
        if (file.size && file.size < MIN_BYTES) {
            fileWarning.style.display = 'block';
            fileWarning.innerText = 'The selected file is very small and may not contain a valid resume. Upload a larger file (recommended > 2 KB).';
            return;
        } else {
            fileWarning.style.display = 'none';
            fileWarning.innerText = '';
        }

        loading.style.display = 'block';
        results.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/analyze', { method: 'POST', body: formData });
            const data = await response.json();

            loading.style.display = 'none';
            results.style.display = 'block';

            if (!response.ok) {
                results.innerHTML = `
                    <div class="metric-card">
                        <h3 style="color: #ff4d6d; margin-bottom: 12px;">Analysis Error</h3>
                        <p style="color: #ffffff;">${data.error || data.message || 'Unable to process file.'}</p>
                    </div>`;
                return;
            }

            // Build skills HTML
            let skillsHtml = '';
            if (data.skills && typeof data.skills === 'object') {
                for (const [cat, list] of Object.entries(data.skills)) {
                    if (list && list.length) {
                        skillsHtml += `<div style="margin-bottom:8px;"><strong style="color:#cfe6ff;">${cat}:</strong> ${list.map(s=>`<span class="skill-tag">${s}</span>`).join(' ')}</div>`;
                    }
                }
            } else if (Array.isArray(data.skills) && data.skills.length) {
                skillsHtml = data.skills.map(s => `<span class="skill-tag">${s}</span>`).join('');
            } else {
                skillsHtml = '<span style="color: #ff6b6b;">No specific skills detected</span>';
            }

            const recommendationsHtml = data.recommendations && data.recommendations.length > 0
                ? data.recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('')
                : '<div class="recommendation-item">No specific recommendations</div>';

            const summaryParts = [];
            if (data.word_count) summaryParts.push(`${data.word_count} words`);
            if (data.experience_years) summaryParts.push(`${data.experience_years} years experience`);
            if (data.skill_count) summaryParts.push(`${data.skill_count} skills detected`);

            const conciseSummary = summaryParts.join(' • ') || 'Resume parsed successfully.';

            results.innerHTML = `
                <div class="metric-card">
                    <h3 style="color: #cfe6ff; margin-bottom: 12px;">ATS Compatibility</h3>
                    <div class="score">${data.ats_score}%</div>
                    <p style="color: #9fb0c8; margin-top:6px">${conciseSummary}</p>
                </div>

                <div class="metric-card">
                    <h3 style="color: #cfe6ff; margin-bottom: 12px;">Skills</h3>
                    <div class="skills-grid">${skillsHtml}</div>
                </div>

                <div class="metric-card">
                    <h3 style="color: #cfe6ff; margin-bottom: 12px;">Recommendations</h3>
                    ${recommendationsHtml}
                </div>
            `;

        } catch (error) {
            loading.style.display = 'none';
            results.innerHTML = `
                <div class="metric-card">
                    <h3 style="color: #ff0080; margin-bottom: 15px;">Connection Error</h3>
                    <p style="color: #ffffff;">Unable to analyze resume. Please try again.</p>
                </div>`;
            console.error('Error:', error);
        }
    });
});
