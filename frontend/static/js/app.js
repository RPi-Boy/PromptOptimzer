/**
 * Main Application JavaScript
 */

const API_BASE_URL = window.location.origin + '/api';
let token = localStorage.getItem('token');
let username = localStorage.getItem('username');
let uploadedQuestions = [];
let selectedModels = [];
let availableModels = [];
let currentRequestId = null;

// Check authentication on page load
window.addEventListener('DOMContentLoaded', async () => {
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Verify token is still valid
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            window.location.href = '/login';
            return;
        }
        
        const user = await response.json();
        username = user.username;
        document.getElementById('username-display').textContent = `Hello, ${username}`;
        
        // Load available models
        await loadAvailableModels();
        
    } catch (error) {
        console.error('Auth error:', error);
        window.location.href = '/login';
    }
});

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

// Load available models
async function loadAvailableModels() {
    try {
        const response = await fetch(`${API_BASE_URL}/prompt/models`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Failed to load models');
        
        const data = await response.json();
        availableModels = data.models;
        
        renderModelSelection();
        
    } catch (error) {
        console.error('Error loading models:', error);
        document.querySelector('.model-selection-grid').innerHTML = 
            '<p class="error">Failed to load models. Please try again.</p>';
    }
}

// Toggle options panel
function toggleOptions() {
    const panel = document.getElementById('options-panel');
    panel.classList.toggle('active');
}

// Toggle user menu
function toggleUserMenu() {
    const menu = document.getElementById('user-menu');
    const isVisible = menu.style.display === 'block';
    menu.style.display = isVisible ? 'none' : 'block';
}

// Close user menu when clicking outside
document.addEventListener('click', (e) => {
    const userIcon = document.querySelector('.user-icon');
    const userMenu = document.getElementById('user-menu');
    if (userMenu && !userIcon.contains(e.target)) {
        userMenu.style.display = 'none';
    }
});

// Render model selection
function renderModelSelection() {
    const container = document.querySelector('.model-selection-grid');
    
    if (availableModels.length === 0) {
        container.innerHTML = '<p>No models available</p>';
        return;
    }
    
    // Show first 50 models (increased from 20)
    const modelsToShow = availableModels.slice(0, 50);
    
    container.innerHTML = modelsToShow.map(model => `
        <div class="model-option" onclick="toggleModel('${model.id}', '${model.name}')">
            ${model.name}
        </div>
    `).join('');
}

// Toggle model selection
function toggleModel(modelId, modelName) {
    const index = selectedModels.findIndex(m => m.id === modelId);
    
    if (index > -1) {
        // Remove model
        selectedModels.splice(index, 1);
    } else {
        // Add model (max 3)
        if (selectedModels.length >= 3) {
            alert('You can select up to 3 models');
            return;
        }
        selectedModels.push({ id: modelId, name: modelName });
    }
    
    updateModelSelection();
    updateSendButton();
}

// Update model selection display
function updateModelSelection() {
    // Update visual selection
    document.querySelectorAll('.model-option').forEach(option => {
        const modelId = option.onclick.toString().match(/'([^']+)'/)[1];
        if (selectedModels.some(m => m.id === modelId)) {
            option.classList.add('selected');
        } else {
            option.classList.remove('selected');
        }
    });
    
    // Update selected models display
    const display = document.getElementById('selected-models-display');
    if (selectedModels.length === 0) {
        display.innerHTML = '';
        return;
    }
    
    display.innerHTML = selectedModels.map(model => `
        <div class="selected-model-tag">
            ${model.name}
            <span class="remove" onclick="toggleModel('${model.id}', '${model.name}')">×</span>
        </div>
    `).join('');
}

// Handle file upload
document.getElementById('file-upload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    const statusDiv = document.getElementById('upload-status');
    statusDiv.textContent = 'Uploading...';
    statusDiv.className = 'status-message';
    
    try {
        const response = await fetch(`${API_BASE_URL}/prompt/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        const data = await response.json();
        uploadedQuestions = data.questions;
        
        statusDiv.textContent = `✓ Uploaded ${data.question_count} questions from ${data.filename}`;
        statusDiv.className = 'status-message success';
        
        // Populate question dropdown
        const select = document.getElementById('question-select');
        select.disabled = false;
        select.innerHTML = '<option value="">Select a question...</option>' +
            uploadedQuestions.map((q, i) => 
                `<option value="${i}">${q.substring(0, 100)}${q.length > 100 ? '...' : ''}</option>`
            ).join('');
        
        updateSendButton();
        
    } catch (error) {
        statusDiv.textContent = `✗ ${error.message}`;
        statusDiv.className = 'status-message error';
    }
});

// Handle question selection
document.getElementById('question-select').addEventListener('change', (e) => {
    const index = e.target.value;
    const textarea = document.getElementById('selected-question');
    
    if (index === '') {
        textarea.value = '';
    } else {
        textarea.value = uploadedQuestions[index];
    }
    
    updateSendButton();
});

// Update send button state
function updateSendButton() {
    const sendBtn = document.getElementById('send-btn');
    const systemPrompt = document.getElementById('system-prompt').value.trim();
    const selectedQuestion = document.getElementById('selected-question').value.trim();
    const hasModels = selectedModels.length > 0;
    
    sendBtn.disabled = !(systemPrompt && selectedQuestion && hasModels);
}

// Listen for changes in system prompt
document.getElementById('system-prompt').addEventListener('input', updateSendButton);

// Run test
async function runTest() {
    const systemPrompt = document.getElementById('system-prompt').value.trim();
    const question = document.getElementById('selected-question').value.trim();
    
    if (!systemPrompt || !question || selectedModels.length === 0) {
        alert('Please fill in all fields and select at least one model');
        return;
    }
    
    // Show loading overlay
    document.getElementById('loading-overlay').classList.add('active');
    
    try {
        const response = await fetch(`${API_BASE_URL}/prompt/test`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                system_prompt: systemPrompt,
                question: question,
                models: selectedModels.map(m => m.id)
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Test failed');
        }
        
        const data = await response.json();
        currentRequestId = data.request_id;
        
        displayResults(data);
        
        // Enable download button
        document.getElementById('download-all-btn').disabled = false;
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        document.getElementById('loading-overlay').classList.remove('active');
    }
}

// Display results
function displayResults(data) {
    const container = document.getElementById('results-container');
    
    container.innerHTML = data.responses.map(response => {
        if (response.error) {
            return `
                <div class="model-card">
                    <div class="model-card-title">Results for ${response.model}</div>
                    <div class="model-card-response">
                        <strong>Error:</strong> ${response.error}
                    </div>
                    <div class="model-card-footer">
                        <div>
                            <div class="model-card-name">${response.model}</div>
                            <div class="model-card-details">Error occurred</div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        return `
            <div class="model-card">
                <div class="model-card-title">Results for ${response.model}</div>
                <div class="model-card-response">${response.response}</div>
                <div class="model-card-footer">
                    <div>
                        <div class="model-card-name">${response.model.split('/').pop()}</div>
                        <div class="model-card-details">${response.tokens_used} tokens • ${response.time_taken.toFixed(2)}s</div>
                    </div>
                    <button class="model-card-info-btn" onclick="showDetailedInfo('${response.model}', ${JSON.stringify(response).replace(/'/g, "&apos;")})">
                        ℹ
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// Retry a single model
async function retryModel(modelId) {
    const systemPrompt = document.getElementById('system-prompt').value.trim();
    const question = document.getElementById('selected-question').value.trim();
    
    const overlay = document.getElementById('loading-overlay');
    overlay.querySelector('p').textContent = `Retrying ${modelId}...`;
    overlay.classList.add('active');
    
    try {
        const response = await fetch(`${API_BASE_URL}/prompt/test/${encodeURIComponent(modelId)}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                system_prompt: systemPrompt,
                question: question,
                models: [modelId]
            })
        });
        
        if (!response.ok) throw new Error('Retry failed');
        
        const data = await response.json();
        
        // Update only that model's result
        const container = document.getElementById('results-container');
        const modelCards = container.querySelectorAll('.model-response');
        
        modelCards.forEach(card => {
            const modelName = card.querySelector('.model-name').textContent.trim();
            if (modelName.includes(modelId) || modelId.includes(modelName)) {
                // Reconstruct the card with new data
                const newCard = document.createElement('div');
                newCard.innerHTML = createModelCard(data);
                card.replaceWith(newCard.firstElementChild);
            }
        });
        
    } catch (error) {
        alert(`Retry error: ${error.message}`);
    } finally {
        overlay.classList.remove('active');
        overlay.querySelector('p').textContent = 'Running tests on selected models...';
    }
}

// Show detailed info modal
function showDetailedInfo(modelName, responseData) {
    const modal = document.getElementById('info-modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    title.textContent = `Detailed Information: ${modelName}`;
    
    body.innerHTML = `
        <div style="margin-bottom: 1.5rem;">
            <h3 style="margin-bottom: 0.5rem;">Response</h3>
            <div style="background: #f5f5f5; padding: 1rem; border-radius: 6px; white-space: pre-wrap; max-height: 300px; overflow-y: auto;">
                ${responseData.response}
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div>
                <strong>Total Tokens:</strong> ${responseData.tokens_used}
            </div>
            <div>
                <strong>Prompt Tokens:</strong> ${responseData.prompt_tokens}
            </div>
            <div>
                <strong>Completion Tokens:</strong> ${responseData.completion_tokens}
            </div>
            <div>
                <strong>Time Taken:</strong> ${responseData.time_taken.toFixed(3)}s
            </div>
            ${responseData.finish_reason ? `
            <div>
                <strong>Finish Reason:</strong> ${responseData.finish_reason}
            </div>
            ` : ''}
            ${responseData.cost ? `
            <div>
                <strong>Cost:</strong> $${responseData.cost}
            </div>
            ` : ''}
        </div>
    `;
    
    modal.classList.add('active');
}

// Close modal
function closeModal() {
    document.getElementById('info-modal').classList.remove('active');
}

// Download all results
function downloadAll() {
    if (!currentRequestId) return;
    
    const url = `${API_BASE_URL}/prompt/download/${currentRequestId}?format=json`;
    downloadFile(url, `prompt_test_${currentRequestId}.json`);
}

// Download single model result
function downloadSingle(modelId) {
    if (!currentRequestId) return;
    
    const url = `${API_BASE_URL}/prompt/download/${currentRequestId}?format=json&model=${encodeURIComponent(modelId)}`;
    downloadFile(url, `prompt_test_${modelId}_${currentRequestId}.json`);
}

// Helper function to download file
async function downloadFile(url, filename) {
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Download failed');
        
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);
        
    } catch (error) {
        alert(`Download error: ${error.message}`);
    }
}

// Helper to create model card HTML
function createModelCard(response) {
    if (response.error) {
        return `
            <div class="model-response">
                <div class="model-response-header">
                    <div class="model-name">${response.model}</div>
                </div>
                <div class="model-error">
                    <strong>Error:</strong> ${response.error}
                </div>
            </div>
        `;
    }
    
    return `
        <div class="model-response">
            <div class="model-response-header">
                <div class="model-name">
                    ${response.model}
                    <button class="info-btn" onclick="showDetailedInfo('${response.model}', ${JSON.stringify(response).replace(/'/g, "&apos;")})">ℹ️</button>
                </div>
                <div class="model-response-actions">
                    <button class="btn btn-secondary" onclick="retryModel('${response.model}')">
                        🔄 Retry
                    </button>
                    <button class="btn btn-secondary" onclick="downloadSingle('${response.model}')">
                        ⬇️
                    </button>
                </div>
            </div>
            <div class="model-response-content">${response.response}</div>
            <div class="model-metrics">
                <div class="metric">
                    <div class="metric-label">Tokens</div>
                    <div class="metric-value">${response.tokens_used}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Prompt</div>
                    <div class="metric-value">${response.prompt_tokens}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Completion</div>
                    <div class="metric-value">${response.completion_tokens}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Time (s)</div>
                    <div class="metric-value">${response.time_taken.toFixed(2)}</div>
                </div>
            </div>
        </div>
    `;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('info-modal');
    if (event.target === modal) {
        closeModal();
    }
}
