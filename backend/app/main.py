"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .core.config import settings
from .core.database import init_db
from .api import auth, prompt

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A web application for optimizing prompts across multiple LLM models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(prompt.router, prefix="/api")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "../../frontend/static")
templates_path = os.path.join(os.path.dirname(__file__), "../../frontend/templates")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"🚀 {settings.APP_NAME} is starting...")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🌐 CORS Origins: {settings.allowed_origins_list}")


@app.get("/")
async def root():
    """Serve the main application page"""
    index_path = os.path.join(templates_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Prompt Optimizer API", "docs": "/docs"}


@app.get("/login")
async def login_page():
    """Serve the login page"""
    login_path = os.path.join(templates_path, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path)
    return {"message": "Login page not found"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
