# Deployment Guide

## Overview
This guide covers deploying the Prompt Optimizer application using Docker.

## Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (optional, for easier management)
- OpenRouter API key

## Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your configuration:**
   ```bash
   # Required: Add your OpenRouter API key
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   
   # Optional: Customize other settings
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DEBUG=False
   ```

## Deployment Options

### Option 1: Docker Compose (Recommended)

**Start the application:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the application:**
```bash
docker-compose down
```

**Rebuild after code changes:**
```bash
docker-compose up -d --build
```

### Option 2: Docker CLI

**Build the image:**
```bash
docker build -t prompt-optimizer .
```

**Run the container:**
```bash
docker run -d \
  -p 8000:8000 \
  --name prompt-optimizer \
  --env-file .env \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/prompt_optimizer.db:/app/prompt_optimizer.db \
  prompt-optimizer
```

**View logs:**
```bash
docker logs -f prompt-optimizer
```

**Stop the container:**
```bash
docker stop prompt-optimizer
docker rm prompt-optimizer
```

## Accessing the Application

Once deployed, access the application at:
- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Initial Setup

1. Navigate to http://localhost:8000
2. You'll be redirected to the login page
3. Click "Register" to create a new account
4. After registration, log in with your credentials
5. Update your OpenRouter API key by clicking the user icon in the top right

## Features Implemented

### ✅ API Key Management
- Click the user icon in the top right corner
- Select "Update API Key"
- Enter your new OpenRouter API key
- The key is updated for the current session

### ✅ Card Expansion
- Click the "ℹ" button on any result card
- View detailed information including:
  - Full response text
  - Model name
  - Time taken
  - Total tokens used
  - Prompt tokens
  - Completion tokens
  - Finish reason (if available)
  - Cost (if available)

### ✅ Model Selection
- 20 pre-selected popular models available
- Models are loaded from `backend/models/model_list.json`
- To customize the model list, edit this file and restart the application

### ✅ Dark Theme
- Modern dark theme with gradient background
- Subtle animations throughout the UI
- Responsive design for all screen sizes

### ✅ Security
- XSS protection with HTML escaping
- SQL injection prevention (using SQLAlchemy ORM)
- JWT authentication for API access
- Password hashing with bcrypt

## Troubleshooting

### Container won't start
- Check if port 8000 is already in use
- Verify your `.env` file exists and has valid values
- Check logs: `docker-compose logs` or `docker logs prompt-optimizer`

### Database errors
- Delete the database file and restart: `rm prompt_optimizer.db && docker-compose restart`

### API key errors
- Ensure your OpenRouter API key is valid
- Update the key through the UI or in the `.env` file

## Production Considerations

For production deployment:

1. **Use a proper database:**
   - Replace SQLite with PostgreSQL or MySQL
   - Update `DATABASE_URL` in `.env`

2. **Enable HTTPS:**
   - Use a reverse proxy (nginx, Caddy, Traefik)
   - Configure SSL certificates

3. **Set strong secrets:**
   - Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
   - Never commit these to version control

4. **Configure CORS:**
   - Update `ALLOWED_ORIGINS` in `.env` for your domain

5. **Use a process manager:**
   - Consider using Docker Swarm or Kubernetes for orchestration

## Monitoring

Check application health:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "Prompt Optimizer",
  "version": "1.0.0"
}
```

## Backup

Backup important data:
```bash
# Database
cp prompt_optimizer.db prompt_optimizer.db.backup

# Uploads
tar -czf uploads_backup.tar.gz uploads/
```

## Support

For issues or questions, please check the main README.md file or create an issue in the repository.
