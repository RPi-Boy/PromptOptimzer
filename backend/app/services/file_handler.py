"""
File handling service for uploading and parsing question files
"""
import json
import os
from typing import List
from fastapi import UploadFile, HTTPException, status
from ..core.config import settings


class FileHandlerService:
    """Service for handling file uploads and parsing"""
    
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file"""
        # Check file extension
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.allowed_extensions_list)}"
            )
    
    @staticmethod
    async def parse_questions(file: UploadFile) -> List[str]:
        """
        Parse questions from uploaded file
        
        Args:
            file: Uploaded file (JSON or TXT)
            
        Returns:
            List of questions
        """
        FileHandlerService.validate_file(file)
        
        content = await file.read()
        file_ext = file.filename.split(".")[-1].lower()
        
        try:
            if file_ext == "json":
                # Parse JSON file
                data = json.loads(content.decode("utf-8"))
                
                # Handle different JSON structures
                if isinstance(data, list):
                    # List of strings or objects
                    questions = []
                    for item in data:
                        if isinstance(item, str):
                            questions.append(item)
                        elif isinstance(item, dict):
                            # Try to find question field
                            question = (
                                item.get("question") or 
                                item.get("text") or 
                                item.get("prompt") or
                                item.get("content") or
                                str(item)
                            )
                            questions.append(question)
                    return questions
                    
                elif isinstance(data, dict):
                    # Dictionary with questions array
                    if "questions" in data:
                        return FileHandlerService._extract_questions(data["questions"])
                    else:
                        # Convert dict values to questions
                        return [str(v) for v in data.values()]
                        
                else:
                    raise ValueError("Invalid JSON structure")
                    
            elif file_ext == "txt":
                # Parse text file - one question per line
                text = content.decode("utf-8")
                questions = [
                    line.strip() 
                    for line in text.split("\n") 
                    if line.strip()
                ]
                return questions
                
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error parsing file: {str(e)}"
            )
    
    @staticmethod
    def _extract_questions(items: list) -> List[str]:
        """Helper to extract questions from list items"""
        questions = []
        for item in items:
            if isinstance(item, str):
                questions.append(item)
            elif isinstance(item, dict):
                question = (
                    item.get("question") or 
                    item.get("text") or 
                    item.get("prompt") or
                    item.get("content") or
                    str(item)
                )
                questions.append(question)
        return questions
    
    @staticmethod
    async def save_file(file: UploadFile) -> str:
        """
        Save uploaded file to disk
        
        Args:
            file: Uploaded file
            
        Returns:
            Filepath where file was saved
        """
        FileHandlerService.validate_file(file)
        
        # Create unique filename
        import uuid
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        
        # Reset file pointer
        await file.seek(0)
        
        return filepath


# Create service instance
file_handler_service = FileHandlerService()
