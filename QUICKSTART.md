# Quick Start Guide

Get up and running with Prompt Optimizer in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

## Installation (3 steps)

### 1. Setup Environment

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Copy configuration template

### 2. Configure API Key

Edit the `.env` file and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your-api-key-here
```

Generate secret keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add them to `.env`:
```env
SECRET_KEY=your-generated-secret-key
JWT_SECRET_KEY=your-generated-jwt-secret-key
```

### 3. Start the Application

```bash
# Linux/Mac
./run.sh

# Windows
run.bat

# Or manually
cd backend
python -m app.main
```

## First Use

1. **Open Browser**: http://localhost:8000
2. **Register**: Create your account
3. **Login**: Sign in with your credentials
4. **Upload Questions**: Click "Upload File" (try the samples in `docs/SAMPLE_QUESTIONS.md`)
5. **Configure**: 
   - Enter system prompt
   - Select a question
   - Choose up to 3 models
6. **Test**: Click "Run Test" and wait for results
7. **Analyze**: Review responses, metrics, and download results

## Sample Test

**System Prompt:**
```
You are a helpful assistant that provides clear and concise explanations.
```

**Question:**
```
What is artificial intelligence?
```

**Models to try:**
- openai/gpt-3.5-turbo
- anthropic/claude-2
- meta-llama/llama-2-70b-chat

## Troubleshooting

**Issue: Can't start server**
- Check if port 8000 is available
- Verify .env file has required keys

**Issue: No models loading**
- Verify OpenRouter API key
- Check internet connection

**Issue: Authentication errors**
- Clear browser localStorage
- Re-login to get fresh token

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for advanced setup
- Review [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API details

## Need Help?

- Check the [Troubleshooting section](docs/SETUP_GUIDE.md#troubleshooting) in the setup guide
- Review error messages in the terminal
- Verify all configuration is correct

---

**That's it! You're ready to optimize prompts! 🚀**
