"""
Pydantic schemas for prompt testing requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ModelSelection(BaseModel):
    """Schema for model selection"""
    model_id: str
    model_name: str


class PromptTestRequest(BaseModel):
    """Schema for prompt testing request"""
    system_prompt: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    models: List[str] = Field(..., min_items=1, max_items=3)


class ModelResponse(BaseModel):
    """Schema for individual model response"""
    model: str
    response: str
    tokens_used: int
    prompt_tokens: int
    completion_tokens: int
    time_taken: float
    cost: Optional[float] = None
    finish_reason: Optional[str] = None
    error: Optional[str] = None


class PromptTestResponse(BaseModel):
    """Schema for prompt testing response"""
    request_id: str
    system_prompt: str
    question: str
    responses: List[ModelResponse]
    total_time: float
    timestamp: datetime


class FileUploadResponse(BaseModel):
    """Schema for file upload response"""
    filename: str
    questions: List[str]
    question_count: int


class DownloadRequest(BaseModel):
    """Schema for download request"""
    model: Optional[str] = None  # If None, download all models
    format: str = "json"  # json or csv
