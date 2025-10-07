# Prompt Optimizer 🚀

A modern web application for testing and optimizing prompts across multiple LLM models in parallel. Built with FastAPI backend and vanilla JavaScript frontend.

## Features ✨

- **User Authentication**: Secure JWT-based authentication system
- **File Upload**: Upload test questions from JSON or TXT files
- **Multi-Model Testing**: Test prompts across up to 3 models simultaneously
- **Parallel Execution**: All models run in parallel for faster results
- **Detailed Metrics**: View tokens used, time taken, and other metrics for each model
- **Individual Retry**: Regenerate responses from specific models
- **Download Results**: Export results in JSON or CSV format
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, intuitive interface with real-time updates

## Technology Stack 🛠️

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **JWT**: Secure token-based authentication
- **httpx/aiohttp**: Async HTTP clients for parallel API calls
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **HTML5/CSS3**: Semantic markup and modern styling
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-first approach

### External APIs
- **OpenRouter**: Access to multiple LLM models

## Project Structure 📁

```
PromptOptimzer/
├── backend/
│   └── app/
│       ├── api/              # API routes
│       │   ├── auth.py       # Authentication endpoints
│       │   └── prompt.py     # Prompt testing endpoints
│       ├── core/             # Core functionality
│       │   ├── config.py     # Configuration management
│       │   ├── database.py   # Database setup
│       │   └── security.py   # Security utilities
│       ├── models/           # Database models
│       │   └── user.py       # User model
│       ├── schemas/          # Pydantic schemas
│       │   ├── user.py       # User schemas
│       │   └── prompt.py     # Prompt schemas
│       ├── services/         # Business logic
│       │   ├── auth.py       # Auth service
│       │   ├── file_handler.py  # File handling
│       │   └── openrouter.py    # OpenRouter integration
│       └── main.py           # Application entry point
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css    # Application styles
│   │   └── js/
│   │       ├── auth.js       # Authentication logic
│   │       └── app.js        # Main application logic
│   └── templates/
│       ├── login.html        # Login/Register page
│       └── index.html        # Dashboard
├── docs/                     # Documentation
├── uploads/                  # Uploaded files storage
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Getting Started 🚀

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PromptOptimzer
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and fill in your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   ```

5. **Run the application**
   ```bash
   cd backend
   python -m app.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - You'll be redirected to the login page
   - Register a new account to get started

## Usage Guide 📖

### 1. Register/Login
- Navigate to the login page
- Create a new account or login with existing credentials

### 2. Upload Questions
- Click the "Upload File" button
- Select a JSON or TXT file containing your test questions
- Supported formats:
  - **JSON**: Array of strings or objects with question fields
  - **TXT**: One question per line

Example JSON format:
```json
[
  "What is the capital of France?",
  "Explain quantum computing in simple terms.",
  "Write a haiku about programming."
]
```

Or:
```json
{
  "questions": [
    {"question": "What is AI?"},
    {"text": "Explain machine learning."}
  ]
}
```

### 3. Configure System Prompt
- Enter your system prompt in the text area
- This sets the context for all model interactions

### 4. Select Question
- Choose a question from the dropdown
- The selected question will appear in the text field
- You can also manually edit the question

### 5. Select Models
- Choose up to 3 models from the available list
- Selected models will appear as tags below the selection area

### 6. Run Test
- Click "Run Test" to execute the prompt across selected models
- All models run in parallel for faster results
- View responses, tokens used, and timing information

### 7. Analyze Results
- Review responses from each model
- Click the ℹ️ icon for detailed information
- Use the 🔄 button to retry a specific model
- Download results using the ⬇️ buttons

## API Endpoints 📡

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Prompt Testing
- `POST /api/prompt/upload` - Upload questions file
- `POST /api/prompt/test` - Test prompt across models
- `POST /api/prompt/test/{model}` - Test single model (retry)
- `GET /api/prompt/models` - Get available models
- `GET /api/prompt/download/{request_id}` - Download results

## Configuration ⚙️

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Prompt Optimizer |
| `DEBUG` | Debug mode | False |
| `SECRET_KEY` | Application secret key | **Required** |
| `JWT_SECRET_KEY` | JWT signing key | **Required** |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 |
| `DATABASE_URL` | Database connection string | sqlite:///./prompt_optimizer.db |
| `OPENROUTER_API_KEY` | OpenRouter API key | **Required** |
| `MAX_UPLOAD_SIZE_MB` | Max file upload size | 10 |
| `ALLOWED_EXTENSIONS` | Allowed file types | json,txt |

## Development 💻

### Running in Development Mode

```bash
# With auto-reload
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Database Migrations

The application uses SQLAlchemy and will automatically create tables on first run. For production, consider using Alembic for migrations.

## Security 🔒

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- Environment variables for sensitive data
- CORS protection
- Input validation using Pydantic
- SQL injection protection via SQLAlchemy ORM

## Performance Optimization ⚡

- Async/await for non-blocking operations
- Parallel model execution using asyncio
- Connection pooling for database
- Static file caching
- Efficient query design

## Troubleshooting 🔧

### Common Issues

**Issue**: Application won't start
- Check if `.env` file exists and has required variables
- Verify Python version (3.9+)
- Ensure all dependencies are installed

**Issue**: Authentication not working
- Verify JWT_SECRET_KEY is set
- Check token expiration settings
- Clear browser localStorage and try again

**Issue**: Models not loading
- Verify OPENROUTER_API_KEY is correct
- Check internet connection
- Review OpenRouter API status

**Issue**: File upload fails
- Check file format (JSON or TXT only)
- Verify file size under MAX_UPLOAD_SIZE_MB
- Ensure uploads/ directory exists and is writable

## Deployment 🚢

### Production Considerations

1. **Environment Variables**
   - Use strong, random secret keys
   - Set DEBUG=False
   - Configure proper CORS origins

2. **Database**
   - Switch to PostgreSQL for production
   - Setup regular backups
   - Use connection pooling

3. **Web Server**
   - Use gunicorn or similar WSGI server
   - Setup nginx as reverse proxy
   - Enable HTTPS/SSL

4. **Monitoring**
   - Implement logging
   - Setup error tracking (e.g., Sentry)
   - Monitor API usage and costs

### Example Production Deployment

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For support, please open an issue in the repository or contact the development team.

## Acknowledgments 🙏

- FastAPI for the amazing web framework
- OpenRouter for multi-model API access
- The open-source community for inspiration and tools

---

Built with ❤️ for prompt optimization
