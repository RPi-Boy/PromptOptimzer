#!/bin/bash

# Prompt Optimizer - Startup Script

echo "🚀 Starting Prompt Optimizer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your API keys!"
    echo "   - OPENROUTER_API_KEY"
    echo "   - SECRET_KEY"
    echo "   - JWT_SECRET_KEY"
    echo ""
    read -p "Press Enter after you've configured .env..."
fi

# Start the application
echo "🌐 Starting server..."
echo "Application will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python -m app.main
