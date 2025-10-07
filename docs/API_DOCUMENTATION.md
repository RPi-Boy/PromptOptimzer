# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication via JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## Authentication Endpoints

### Register User
Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "string (min: 3, max: 50)",
  "email": "string (valid email)",
  "password": "string (min: 6)"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400 Bad Request`: Username or email already exists
- `422 Unprocessable Entity`: Validation error

---

### Login
Authenticate and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account is inactive

---

### Get Current User
Retrieve authenticated user information.

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

## Prompt Testing Endpoints

### Upload Questions File
Upload a file containing test questions.

**Endpoint:** `POST /prompt/upload`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: File (JSON or TXT, max 10MB)

**Supported File Formats:**

JSON (Array of strings):
```json
[
  "What is AI?",
  "Explain machine learning."
]
```

JSON (Array of objects):
```json
[
  {"question": "What is AI?"},
  {"text": "Explain ML."}
]
```

JSON (Object with questions key):
```json
{
  "questions": ["What is AI?", "Explain ML."]
}
```

TXT (One question per line):
```
What is AI?
Explain machine learning.
```

**Response:** `200 OK`
```json
{
  "filename": "questions.json",
  "questions": [
    "What is AI?",
    "Explain machine learning."
  ],
  "question_count": 2
}
```

**Error Responses:**
- `400 Bad Request`: Invalid file format or no questions found
- `413 Payload Too Large`: File exceeds size limit

---

### Test Prompt Across Models
Execute a prompt test across multiple selected models in parallel.

**Endpoint:** `POST /prompt/test`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "system_prompt": "You are a helpful assistant.",
  "question": "What is the capital of France?",
  "models": [
    "openai/gpt-3.5-turbo",
    "anthropic/claude-2",
    "meta-llama/llama-2-70b-chat"
  ]
}
```

**Constraints:**
- `system_prompt`: Required, min length 1
- `question`: Required, min length 1
- `models`: Required, min 1 model, max 3 models

**Response:** `200 OK`
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "system_prompt": "You are a helpful assistant.",
  "question": "What is the capital of France?",
  "responses": [
    {
      "model": "openai/gpt-3.5-turbo",
      "response": "The capital of France is Paris.",
      "tokens_used": 45,
      "prompt_tokens": 20,
      "completion_tokens": 25,
      "time_taken": 1.234,
      "cost": 0.00045,
      "finish_reason": "stop",
      "error": null
    },
    {
      "model": "anthropic/claude-2",
      "response": "Paris is the capital city of France.",
      "tokens_used": 42,
      "prompt_tokens": 18,
      "completion_tokens": 24,
      "time_taken": 1.567,
      "cost": null,
      "finish_reason": "end_turn",
      "error": null
    }
  ],
  "total_time": 1.6,
  "timestamp": "2024-01-01T12:00:00"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or expired token

---

### Test Single Model (Retry)
Test a single model, typically used for retry/regenerate functionality.

**Endpoint:** `POST /prompt/test/{model}`

**Path Parameters:**
- `model`: Model identifier (URL encoded)

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "system_prompt": "You are a helpful assistant.",
  "question": "What is the capital of France?",
  "models": ["openai/gpt-3.5-turbo"]
}
```

**Response:** `200 OK`
```json
{
  "model": "openai/gpt-3.5-turbo",
  "response": "The capital of France is Paris.",
  "tokens_used": 45,
  "prompt_tokens": 20,
  "completion_tokens": 25,
  "time_taken": 1.234,
  "cost": 0.00045,
  "finish_reason": "stop",
  "error": null
}
```

**Error Responses:**
- `400 Bad Request`: Invalid model or request
- `401 Unauthorized`: Invalid or expired token

---

### Get Available Models
Retrieve list of available models from OpenRouter.

**Endpoint:** `GET /prompt/models`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "models": [
    {
      "id": "openai/gpt-3.5-turbo",
      "name": "GPT-3.5 Turbo",
      "description": "Fast and efficient model from OpenAI",
      "context_length": 4096,
      "pricing": {
        "prompt": "0.0015",
        "completion": "0.002"
      }
    },
    {
      "id": "anthropic/claude-2",
      "name": "Claude 2",
      "description": "Anthropic's conversational AI",
      "context_length": 100000,
      "pricing": {
        "prompt": "0.008",
        "completion": "0.024"
      }
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token
- `503 Service Unavailable`: Unable to fetch models from OpenRouter

---

### Download Test Results
Download test results in JSON or CSV format.

**Endpoint:** `GET /prompt/download/{request_id}`

**Path Parameters:**
- `request_id`: UUID of the test request

**Query Parameters:**
- `format`: Download format (`json` or `csv`), default: `json`
- `model`: Optional model filter (if specified, downloads only that model's results)

**Headers:**
```
Authorization: Bearer <token>
```

**Example URLs:**
```
# Download all results as JSON
GET /prompt/download/550e8400-e29b-41d4-a716-446655440000?format=json

# Download single model as CSV
GET /prompt/download/550e8400-e29b-41d4-a716-446655440000?format=csv&model=openai/gpt-3.5-turbo
```

**Response:** `200 OK`

**Content-Type:** 
- `application/json` for JSON format
- `text/csv` for CSV format

**JSON Response:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "system_prompt": "You are a helpful assistant.",
  "question": "What is the capital of France?",
  "responses": [...],
  "total_time": 1.6,
  "timestamp": "2024-01-01T12:00:00"
}
```

**CSV Response:**
```csv
Model,Response,Tokens Used,Prompt Tokens,Completion Tokens,Time Taken (s),Cost,Finish Reason,Error
openai/gpt-3.5-turbo,"The capital of France is Paris.",45,20,25,1.23,0.00045,stop,
```

**Error Responses:**
- `400 Bad Request`: Invalid format specified
- `404 Not Found`: Request ID not found or no results for specified model
- `401 Unauthorized`: Invalid or expired token

---

## Error Response Format

All error responses follow this structure:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `413 Payload Too Large`: File size exceeds limit
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: External service unavailable

---

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting based on:
- Requests per minute per user
- Concurrent model tests per user
- File upload frequency

---

## WebSocket Support

Currently not implemented. Future versions may include WebSocket support for:
- Real-time model response streaming
- Live token usage updates
- Progress indicators for long-running tests

---

## Authentication Flow

1. **Register**: `POST /auth/register` → Receive user data
2. **Login**: `POST /auth/login` → Receive JWT token
3. **Store Token**: Save token in localStorage/sessionStorage
4. **Make Requests**: Include token in Authorization header
5. **Token Expiration**: Token expires after 30 minutes (default)
6. **Refresh**: Login again when token expires

---

## Best Practices

1. **Token Storage**: Store JWT tokens securely (httpOnly cookies or secure storage)
2. **Error Handling**: Always handle error responses appropriately
3. **Parallel Requests**: Use batch endpoints when testing multiple models
4. **File Size**: Keep uploaded files under the size limit
5. **Caching**: Cache available models list to reduce API calls
6. **Timeouts**: Set appropriate timeouts for model testing (can take 30-60 seconds)

---

## Example Integration

### JavaScript/Fetch Example

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user', password: 'pass' })
});
const { access_token } = await loginResponse.json();

// Test prompt
const testResponse = await fetch('http://localhost:8000/api/prompt/test', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    system_prompt: 'You are helpful.',
    question: 'What is AI?',
    models: ['openai/gpt-3.5-turbo']
  })
});
const results = await testResponse.json();
```

### Python/httpx Example

```python
import httpx

# Login
response = httpx.post(
    'http://localhost:8000/api/auth/login',
    json={'username': 'user', 'password': 'pass'}
)
token = response.json()['access_token']

# Test prompt
response = httpx.post(
    'http://localhost:8000/api/prompt/test',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'system_prompt': 'You are helpful.',
        'question': 'What is AI?',
        'models': ['openai/gpt-3.5-turbo']
    }
)
results = response.json()
```

---

For more information, see the [README.md](../README.md) file.
