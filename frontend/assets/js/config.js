/**
 * AI Resume Analyzer - Frontend Configuration
 * Manages API endpoint detection with override support
 */

(function () {
    // Default production API endpoint
    const DEFAULT_API = '/api/analyze';
    const LOCAL_API = 'http://127.0.0.1:5000/analyze';
    
    // Try to detect if we're on Vercel or local
    function getApiEndpoint() {
        const hostname = window.location.hostname;
        
        // Check for query parameter override
        const params = new URLSearchParams(window.location.search);
        const apiOverride = params.get('api');
        if (apiOverride) {
            try {
                localStorage.setItem('API_OVERRIDE', apiOverride);
            } catch (e) {}
            console.log('✅ Using API override from query param:', apiOverride);
            return apiOverride;
        }
        
        // Check for localStorage override
        try {
            const stored = localStorage.getItem('API_OVERRIDE');
            if (stored) {
                console.log('✅ Using API override from localStorage:', stored);
                return stored;
            }
        } catch (e) {}
        
        // If running locally, use local API
        if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.startsWith('127.')) {
            console.log('✅ Local development detected, using:', LOCAL_API);
            return LOCAL_API;
        }
        
        // Default to Vercel API (same domain as frontend)
        console.log('✅ Production environment, using:', DEFAULT_API);
        return DEFAULT_API;
    }
    
    window.API_ENDPOINT = getApiEndpoint();
    console.log('🔧 API Endpoint configured:', window.API_ENDPOINT);
})();
