# Setup Guide

This guide will walk you through setting up the Prompt Optimizer application from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [First-Time Setup](#first-time-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Comes with Python
- **Git**: [Download Git](https://git-scm.com/downloads)

### Required API Keys
- **OpenRouter API Key**: 
  1. Go to [OpenRouter](https://openrouter.ai/)
  2. Sign up for an account
  3. Navigate to [API Keys](https://openrouter.ai/keys)
  4. Generate a new API key
  5. Copy and save it securely

### System Requirements
- **RAM**: Minimum 2GB, recommended 4GB+
- **Disk Space**: 500MB free space
- **Network**: Stable internet connection for API calls

---

## Installation

### Step 1: Clone or Download Repository

If using Git:
```bash
git clone <repository-url>
cd PromptOptimzer
```

Or download and extract the ZIP file, then navigate to the directory.

### Step 2: Create Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required Python packages including:
- FastAPI
- Uvicorn
- SQLAlchemy
- JWT libraries
- HTTP clients
- And more

**Expected installation time:** 2-5 minutes depending on your internet speed.

### Step 4: Verify Installation

```bash
python -c "import fastapi; import uvicorn; import sqlalchemy; print('All packages installed successfully!')"
```

If you see the success message, you're good to go!

---

## Configuration

### Step 1: Create Environment File

Copy the example environment file:
```bash
cp .env.example .env
```

**On Windows:**
```bash
copy .env.example .env
```

### Step 2: Generate Secret Keys

You need secure random keys for production. Generate them using Python:

```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Copy these values for the next step.

### Step 3: Edit .env File

Open `.env` in your text editor and update the following variables:

```env
# Application Settings
APP_NAME=Prompt Optimizer
DEBUG=True
SECRET_KEY=<paste-generated-secret-key-here>

# Database
DATABASE_URL=sqlite:///./prompt_optimizer.db

# OpenRouter API
OPENROUTER_API_KEY=<paste-your-openrouter-api-key-here>

# JWT Settings
JWT_SECRET_KEY=<paste-generated-jwt-secret-key-here>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# File Upload Settings
MAX_UPLOAD_SIZE_MB=10
ALLOWED_EXTENSIONS=json,txt

# Server Settings
HOST=0.0.0.0
PORT=8000
```

**Important:**
- Replace `<paste-your-openrouter-api-key-here>` with your actual OpenRouter API key
- Replace the secret keys with the generated values
- For production, set `DEBUG=False`

### Step 4: Verify Configuration

```bash
python -c "from backend.app.core.config import settings; print(f'App: {settings.APP_NAME}'); print('Config loaded successfully!')"
```

---

## Running the Application

### Development Mode (with auto-reload)

**From project root:**
```bash
cd backend
python -m app.main
```

**Or using uvicorn directly:**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

**On Windows, you might need:**
```bash
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Install gunicorn (Linux/Mac only)
pip install gunicorn

# Run with gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Accessing the Application

Once running, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Open your browser and navigate to:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## First-Time Setup

### 1. Database Initialization

The database is automatically created on first run. You should see:
```
🚀 Prompt Optimizer is starting...
📊 Database: sqlite:///./prompt_optimizer.db
```

The SQLite database file `prompt_optimizer.db` will be created in your backend directory.

### 2. Register Your First User

1. Navigate to http://localhost:8000
2. You'll be redirected to the login page
3. Click "Register"
4. Fill in the registration form:
   - **Username**: Choose a username (min 3 characters)
   - **Email**: Your email address
   - **Password**: Choose a secure password (min 6 characters)
   - **Confirm Password**: Re-enter password
5. Click "Register"
6. You'll see a success message
7. The page will automatically redirect to login

### 3. Login

1. Enter your username and password
2. Click "Login"
3. You'll be redirected to the dashboard

### 4. Test the Application

1. **Upload Questions File**:
   - Create a test file `questions.txt`:
     ```
     What is artificial intelligence?
     Explain quantum computing.
     How does blockchain work?
     ```
   - Click "Upload File" and select your file
   - Verify the questions are loaded

2. **Enter System Prompt**:
   ```
   You are a knowledgeable assistant that provides clear and concise explanations.
   ```

3. **Select Question**:
   - Choose a question from the dropdown

4. **Select Models**:
   - Click on up to 3 models
   - Popular choices: GPT-3.5 Turbo, Claude 2, Llama 2

5. **Run Test**:
   - Click "Run Test"
   - Wait for responses (usually 5-30 seconds)
   - Review the results

---

## Troubleshooting

### Issue: Module not found error

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: Can't access application

**Error:** Browser shows "Can't connect to server"

**Solutions:**
1. Check if server is running (look for "Uvicorn running" message)
2. Verify the port isn't in use:
   ```bash
   # Linux/Mac
   lsof -i :8000
   
   # Windows
   netstat -ano | findstr :8000
   ```
3. Try a different port:
   ```bash
   uvicorn backend.app.main:app --reload --port 8001
   ```

---

### Issue: Database errors

**Error:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solutions:**
1. Ensure the backend directory exists
2. Check write permissions
3. Delete existing database and restart:
   ```bash
   rm prompt_optimizer.db
   python -m backend.app.main
   ```

---

### Issue: OpenRouter API errors

**Error:** "Invalid API key" or "OpenRouter connection failed"

**Solutions:**
1. Verify your API key in `.env`:
   ```bash
   cat .env | grep OPENROUTER_API_KEY
   ```
2. Test your API key:
   ```bash
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```
3. Check your OpenRouter account has credits
4. Verify internet connection

---

### Issue: File upload fails

**Error:** "Invalid file type" or "No questions found"

**Solutions:**
1. Check file format (must be .json or .txt)
2. Verify JSON is valid:
   ```bash
   python -m json.tool < your-file.json
   ```
3. Ensure text file has one question per line
4. Check file size (must be under MAX_UPLOAD_SIZE_MB)

---

### Issue: Token expired

**Error:** "Invalid authentication credentials"

**Solutions:**
1. Login again to get a new token
2. Increase token expiration in `.env`:
   ```env
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```
3. Clear browser localStorage:
   ```javascript
   localStorage.clear()
   ```

---

### Issue: CORS errors

**Error:** "CORS policy: No 'Access-Control-Allow-Origin' header"

**Solutions:**
1. Add your frontend URL to `.env`:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000
   ```
2. Restart the server after changing `.env`

---

## Advanced Configuration

### Using PostgreSQL Instead of SQLite

1. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update DATABASE_URL in `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

### Enabling HTTPS/SSL

For production, use a reverse proxy like nginx with SSL certificates.

Example nginx configuration:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Custom Port Configuration

Change the port in `.env`:
```env
PORT=3000
```

Or override when starting:
```bash
uvicorn backend.app.main:app --port 3000
```

---

## Next Steps

- Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Check [README.md](../README.md) for usage guide
- Explore the code structure in the backend directory
- Test different models and prompts
- Export and analyze your results

---

## Getting Help

If you encounter issues not covered here:

1. Check the application logs
2. Review error messages carefully
3. Search for similar issues online
4. Check OpenRouter API status
5. Verify all dependencies are installed correctly

---

## Security Checklist

Before deploying to production:

- [ ] Change all default secret keys
- [ ] Set DEBUG=False
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular backups of database
- [ ] Keep dependencies updated
- [ ] Use environment variables for all secrets

---

Happy prompt optimizing! 🚀
