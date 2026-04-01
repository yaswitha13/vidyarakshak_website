let API_BASE_URL = (window.location.protocol === 'file:') ? 'http://127.0.0.1:5000' : `${window.location.protocol}//${window.location.hostname}:5000`;
if (API_BASE_URL.endsWith('/')) API_BASE_URL = API_BASE_URL.slice(0, -1);

class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

/**
 * Generic request wrapper
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
    if (endpoint.includes('email=null')) {
        console.warn('Blocking API request with "null" email');
        return null;
    }
    
    // Ensure endpoint starts with a single slash
    if (!endpoint.startsWith('/')) endpoint = '/' + endpoint;
    
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

    const config = {
        method,
        headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        // Cache busting for GET requests to ensure fresh data
        const separator = endpoint.includes('?') ? '&' : '?';
        let finalUrl = method === 'GET' ? `${API_BASE_URL}${endpoint}${separator}t=${Date.now()}` : `${API_BASE_URL}${endpoint}`;
        
        // Automaticaly append school_code to GET requests if session exists
        if (method === 'GET' && !endpoint.includes('school_code=')) {
            const sc = localStorage.getItem('schoolCode');
            if (sc) {
                finalUrl += `&school_code=${sc}`;
            }
        }

        const response = await fetch(finalUrl, {
            ...config,
            cache: 'no-cache' // Explicitly disable caching for all requests
        });
        const data = await response.json().catch(() => ({}));
        
        if (!response.ok) {
            throw new ApiError(data.message || 'An error occurred', response.status);
        }
        
        return data;
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// Global UI Helpers
function showAlert(elementId, message, type = 'error') {
    const el = document.getElementById(elementId);
    if (!el) return;
    
    el.textContent = message;
    el.className = `alert alert-${type}`;
    el.style.display = 'block';
    
    setTimeout(() => {
        el.style.display = 'none';
    }, 5000);
}

// Session Management Helpers
function saveSession(userEmail, userRole, schoolCode) {
    localStorage.setItem('userEmail', userEmail);
    localStorage.setItem('userRole', userRole);
    if (schoolCode) localStorage.setItem('schoolCode', schoolCode);
}

function clearSession(force = false) {
    if (!force) {
        if (!confirm('Are you sure you want to sign out?')) {
            return;
        }
    }
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userRole');
    localStorage.removeItem('schoolCode');
    window.location.href = 'index.html';
}

function getSession() {
    return {
        email: localStorage.getItem('userEmail'),
        role: localStorage.getItem('userRole'),
        schoolCode: localStorage.getItem('schoolCode')
    };
}

function requireAuth(expectedRole = null) {
    const session = getSession();
    if (!session.email || !session.role) {
        clearSession(true);
        return null;
    }
    
    if (expectedRole && session.role !== expectedRole) {
        clearSession(true);
        return null;
    }
    
    return session;
}

// --- VALIDATION HELPERS ---

const Validator = {
    email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val),
    phone: (val) => /^[6-9]\d{9}$/.test(val),
    username: (val) => /^[a-zA-Z0-9]{4,}$/.test(val),
    name: (val) => /^[a-zA-Z\s]{3,}$/.test(val),
    required: (val) => val.trim().length > 0
};

function attachValidation(inputId, type) {
    const input = document.getElementById(inputId);
    if (!input) return;

    const wrapper = input.closest('.input-field') || input.closest('.input-wrapper') || input.parentElement;

    const validate = () => {
        const val = input.value;
        if (val.trim() === '') {
            wrapper.classList.remove('is-valid', 'is-invalid');
            return false;
        }

        const isValid = Validator[type](val);
        if (isValid) {
            wrapper.classList.add('is-valid');
            wrapper.classList.remove('is-invalid');
        } else {
            wrapper.classList.add('is-invalid');
            wrapper.classList.remove('is-valid');
        }
        return isValid;
    };

    input.addEventListener('input', validate);
    input.addEventListener('blur', validate);
    
    return validate;
}

// --- ADMIN PROFILE APIs ---

async function fetchAdminProfile(email) {
    return await apiRequest(`/api/admin/profile/${email}`);
}

async function updateAdminProfile(profileData) {
    return await apiRequest('/api/admin/profile/update', 'POST', profileData);
}
