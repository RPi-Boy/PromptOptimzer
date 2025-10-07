"""
Prompt testing API routes
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
import json
import io
import csv
import time
import uuid
from datetime import datetime

from ..schemas.prompt import (
    PromptTestRequest, 
    PromptTestResponse, 
    FileUploadResponse,
    ModelResponse
)
from ..services.openrouter import openrouter_service
from ..services.file_handler import file_handler_service
from ..api.auth import get_current_user_dependency
from ..models.user import User

router = APIRouter(prefix="/prompt", tags=["Prompt Testing"])

# Store recent test results in memory (in production, use Redis or database)
test_results_cache = {}


@router.post("/upload", response_model=FileUploadResponse)
async def upload_questions_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Upload a file containing test questions
    
    Args:
        file: JSON or TXT file with questions
        current_user: Authenticated user
        
    Returns:
        Parsed questions from the file
    """
    questions = await file_handler_service.parse_questions(file)
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No questions found in file"
        )
    
    return FileUploadResponse(
        filename=file.filename,
        questions=questions,
        question_count=len(questions)
    )


@router.post("/test", response_model=PromptTestResponse)
async def test_prompt(
    request: PromptTestRequest,
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Test a prompt with selected question across multiple models
    
    Args:
        request: Prompt test request with system prompt, question, and models
        current_user: Authenticated user
        
    Returns:
        Responses from all selected models with metadata
    """
    start_time = time.time()
    
    # Call models in parallel
    responses = await openrouter_service.call_models_parallel(
        models=request.models,
        system_prompt=request.system_prompt,
        user_message=request.question
    )
    
    total_time = time.time() - start_time
    request_id = str(uuid.uuid4())
    
    # Create response
    result = PromptTestResponse(
        request_id=request_id,
        system_prompt=request.system_prompt,
        question=request.question,
        responses=responses,
        total_time=total_time,
        timestamp=datetime.utcnow()
    )
    
    # Cache result for later download
    test_results_cache[request_id] = result
    
    return result


@router.post("/test/{model}", response_model=ModelResponse)
async def test_single_model(
    model: str,
    request: PromptTestRequest,
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Test a single model (for retry/regenerate functionality)
    
    Args:
        model: Model identifier to test
        request: Prompt test request
        current_user: Authenticated user
        
    Returns:
        Response from the specified model
    """
    response = await openrouter_service.call_model(
        model=model,
        system_prompt=request.system_prompt,
        user_message=request.question
    )
    
    return response


@router.get("/models")
async def get_available_models(
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Get list of available models from OpenRouter
    
    Args:
        current_user: Authenticated user
        
    Returns:
        List of available models
    """
    models = await openrouter_service.get_available_models()
    
    # Return simplified model list
    return {
        "models": [
            {
                "id": model.get("id"),
                "name": model.get("name", model.get("id")),
                "description": model.get("description", ""),
                "context_length": model.get("context_length", 0),
                "pricing": model.get("pricing", {})
            }
            for model in models
        ]
    }


@router.get("/download/{request_id}")
async def download_results(
    request_id: str,
    format: str = "json",
    model: str = None,
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Download test results
    
    Args:
        request_id: ID of the test request
        format: Download format (json or csv)
        model: Optional model filter (if None, download all)
        current_user: Authenticated user
        
    Returns:
        File download response
    """
    # Get cached result
    if request_id not in test_results_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test results not found"
        )
    
    result = test_results_cache[request_id]
    
    # Filter by model if specified
    responses = result.responses
    if model:
        responses = [r for r in responses if r.model == model]
        if not responses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No results found for model: {model}"
            )
    
    if format.lower() == "json":
        # JSON download
        data = {
            "request_id": result.request_id,
            "system_prompt": result.system_prompt,
            "question": result.question,
            "responses": [r.dict() for r in responses],
            "total_time": result.total_time,
            "timestamp": result.timestamp.isoformat()
        }
        
        json_str = json.dumps(data, indent=2)
        filename = f"prompt_test_{request_id}.json"
        
        return StreamingResponse(
            io.BytesIO(json_str.encode()),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    elif format.lower() == "csv":
        # CSV download
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "Model", "Response", "Tokens Used", "Prompt Tokens", 
            "Completion Tokens", "Time Taken (s)", "Cost", "Finish Reason", "Error"
        ])
        
        # Write data
        for r in responses:
            writer.writerow([
                r.model, r.response, r.tokens_used, r.prompt_tokens,
                r.completion_tokens, f"{r.time_taken:.2f}", r.cost or "", 
                r.finish_reason or "", r.error or ""
            ])
        
        filename = f"prompt_test_{request_id}.csv"
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid format. Use 'json' or 'csv'"
        )
