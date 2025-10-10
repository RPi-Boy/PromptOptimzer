# Quick Start Guide - New Features

## 🚀 Getting Started

### Using Docker (Recommended)
```bash
# 1. Set up environment
cp .env.example .env
# Edit .env and add your OpenRouter API key

# 2. Start the application
docker-compose up -d

# 3. Access the application
# Open http://localhost:8000 in your browser
```

### Traditional Method
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env and add your OpenRouter API key

# 3. Run the application
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## 🎨 New Features Overview

### 1. Update OpenRouter API Key
**How to use:**
1. Click the **user icon** in the top right corner
2. Click **"Update API Key"**
3. Enter your new OpenRouter API key
4. Click **"Update Key"**
5. See success confirmation

**When to use:**
- When you get a new API key
- When you want to switch accounts
- For testing with different keys

### 2. View Detailed Results
**How to use:**
1. Run a test with your selected models
2. Click the **ℹ button** on any result card
3. View comprehensive details in the modal:
   - Full response text (scrollable)
   - Model name
   - Time taken
   - Token usage (total, prompt, completion)
   - Finish reason
   - Cost (if available)
4. Click the **× button** or click outside to close

**Tip:** The expanded view is perfect for comparing results in detail!

### 3. Consistent Model Selection
**What's new:**
- 20 pre-selected popular models always available
- Models don't change on page reload
- Includes best models from:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude 3.5, Claude 3)
  - Google (Gemini)
  - Meta (Llama 3.1)
  - Mistral, Cohere, and more!

**Customize models:**
Edit `backend/models/model_list.json` to change the available models.

### 4. Beautiful Dark Theme
**Features:**
- Smooth gradient background animation
- Purple and pink accent colors
- High contrast for readability
- Subtle animations on hover
- Modern glassmorphism effects

**Responsive:**
- Works on desktop, tablet, and mobile
- Adapts layout to screen size
- Touch-friendly on mobile devices

## 🔒 Security Features

### XSS Protection
All user inputs are automatically sanitized to prevent cross-site scripting attacks.

### SQL Injection Prevention
Using SQLAlchemy ORM ensures all database queries are safe from SQL injection.

### Secure Authentication
- JWT tokens for API access
- Password hashing with bcrypt
- Secure session management

## 📊 Model List

Current pre-selected models (20 total):
1. GPT-4 Turbo
2. GPT-4
3. GPT-3.5 Turbo
4. Claude 3.5 Sonnet
5. Claude 3 Opus
6. Claude 3 Sonnet
7. Claude 3 Haiku
8. Gemini Pro 1.5
9. Gemini Pro
10. Llama 3.1 70B
11. Llama 3.1 405B
12. Mistral Large
13. Mixtral 8x7B
14. Command R Plus
15. Perplexity Sonar Large
16. DeepSeek Chat
17. Qwen 2 72B
18. DBRX Instruct
19. Nous Hermes 2 Mixtral
20. WizardLM 2 8x22B

## 🎯 Common Workflows

### Testing Multiple Models
1. Enter your system prompt
2. Upload or select a question
3. Click "Options" to expand the panel
4. Select up to 3 models
5. Click "🚀 Run Test"
6. View results in the cards below
7. Click ℹ on any card for detailed info

### Comparing Results
1. After running a test, results appear in a grid
2. Each card shows:
   - Model name
   - Response preview
   - Token count
   - Time taken
3. Click ℹ to see full details
4. Compare responses side-by-side

### Downloading Results
1. After a test completes
2. Use the download buttons (feature already existed)
3. Choose JSON or CSV format
4. Results include all metadata

## 🐛 Troubleshooting

### API Key Not Working
- Verify the key is correct (starts with `sk-or-`)
- Check OpenRouter dashboard for key status
- Update the key through the UI or `.env` file

### Models Not Loading
- Check `backend/models/model_list.json` exists
- Verify JSON syntax is valid
- Restart the application

### Dark Theme Issues
- Clear browser cache
- Hard reload (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for CSS errors

### Docker Issues
- Ensure port 8000 is not in use
- Check Docker logs: `docker-compose logs`
- Verify `.env` file exists

## 💡 Tips & Tricks

1. **Keyboard Shortcuts:**
   - `Esc` closes modals
   - Click outside modals to close them

2. **Performance:**
   - Selecting fewer models = faster results
   - Use shorter prompts for quicker responses

3. **Best Practices:**
   - Test with multiple models for comparison
   - Keep system prompts concise
   - Review detailed info to understand model behavior

4. **Customization:**
   - Edit `model_list.json` to change available models
   - Adjust `.env` for configuration changes
   - CSS variables in `styles.css` for theme tweaks

## 📚 Additional Resources

- **Full Documentation:** See `README.md`
- **Deployment Guide:** See `DEPLOYMENT.md`
- **Change Log:** See `CHANGES.md`
- **API Docs:** http://localhost:8000/docs (when running)

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify your `.env` configuration
4. Check OpenRouter API status

## 🎉 Enjoy!

The Prompt Optimizer is now more powerful, beautiful, and secure. Happy testing!
