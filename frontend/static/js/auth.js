/**
 * Authentication JavaScript
 */

const API_BASE_URL = window.location.origin + '/api';

// Switch between login and register forms
function switchToRegister() {
    document.getElementById('loginForm').classList.remove('active');
    document.getElementById('registerForm').classList.add('active');
    clearErrors();
}

function switchToLogin() {
    document.getElementById('registerForm').classList.remove('active');
    document.getElementById('loginForm').classList.add('active');
    clearErrors();
}

function clearErrors() {
    document.getElementById('login-error').classList.remove('active');
    document.getElementById('register-error').classList.remove('active');
    document.getElementById('register-success').classList.remove('active');
}

// Handle login form submission
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }
        
        // Store token in localStorage
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', username);
        
        // Redirect to dashboard
        window.location.href = '/';
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('active');
    }
});

// Handle register form submission
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const errorDiv = document.getElementById('register-error');
    const successDiv = document.getElementById('register-success');
    
    // Clear previous messages
    errorDiv.classList.remove('active');
    successDiv.classList.remove('active');
    
    // Validate passwords match
    if (password !== confirmPassword) {
        errorDiv.textContent = 'Passwords do not match';
        errorDiv.classList.add('active');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }
        
        // Show success message
        successDiv.textContent = 'Registration successful! Please login.';
        successDiv.classList.add('active');
        
        // Clear form
        document.getElementById('register-form').reset();
        
        // Switch to login after 2 seconds
        setTimeout(() => {
            switchToLogin();
        }, 2000);
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('active');
    }
});

// Check if already logged in
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token && window.location.pathname === '/login') {
        // Verify token is still valid
        fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            }
        });
    }
});
