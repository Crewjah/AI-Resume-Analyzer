(function(){
  const form = document.getElementById('analyze-form');
  const submitBtn = document.getElementById('submit-btn');
  const resultEl = document.getElementById('result');
  const debugEl = document.getElementById('debug');
  const statusPill = document.getElementById('status-pill');

  const setPill = (text, ok=true) => {
    statusPill.textContent = text;
    statusPill.classList.remove('ok','bad');
    statusPill.classList.add(ok ? 'ok' : 'bad');
  };

  async function checkStatus(){
    try {
      const res = await fetch('/status', { cache: 'no-store' });
      const json = await res.json();
      if(json && json.ready){
        setPill('API Ready', true);
      } else {
        setPill('Analyzer not ready', false);
        if(json && json.error){
          debugEl.textContent = 'Status error: ' + json.error;
        }
      }
    } catch(e){
      setPill('API Unreachable', false);
      debugEl.textContent = 'Status fetch failed: ' + (e && e.message ? e.message : e);
    }
  }

  checkStatus();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultEl.textContent = '';
    debugEl.textContent = '';

    const fileInput = document.getElementById('resume');
    const jdInput = document.getElementById('job');
    const file = fileInput.files && fileInput.files[0];
    if(!file){
      resultEl.textContent = 'Please select a resume file.';
      return;
    }

    submitBtn.disabled = true;
    setPill('Analyzing...', true);

    try {
      const fd = new FormData();
      fd.append('file', file);
      if(jdInput.value) fd.append('job_description', jdInput.value);

      const res = await fetch('/api/analyze', {
        method: 'POST',
        body: fd
      });

      const text = await res.text();
      let json;
      try { json = JSON.parse(text); } catch { json = { raw: text }; }

      if(!res.ok){
        setPill('Error', false);
        resultEl.textContent = 'Error: ' + (json && (json.error || json.raw || res.status));
      } else {
        setPill('Done', true);
        // Pretty print response
        resultEl.innerHTML = '<pre>' + JSON.stringify(json, null, 2) + '</pre>';
      }
    } catch(e){
      setPill('Error', false);
      debugEl.textContent = 'Request failed: ' + (e && e.message ? e.message : e);
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
