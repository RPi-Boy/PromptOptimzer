"""
OpenRouter API service for interacting with multiple LLM models
"""
import httpx
import asyncio
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..core.config import settings
from ..schemas.prompt import ModelResponse


class OpenRouterService:
    """Service for interacting with OpenRouter API"""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self._update_headers()
    
    def _update_headers(self):
        """Update headers with current API key"""
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": settings.APP_NAME
        }
    
    def update_api_key(self, new_api_key: str):
        """Update the API key for this session"""
        self.api_key = new_api_key
        self._update_headers()
    
    async def call_model(
        self, 
        model: str, 
        system_prompt: str, 
        user_message: str
    ) -> ModelResponse:
        """
        Call a single model with the given prompt
        
        Args:
            model: Model identifier (e.g., "openai/gpt-4")
            system_prompt: System prompt to set context
            user_message: User message/question
            
        Returns:
            ModelResponse with the model's response and metadata
        """
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                }
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                time_taken = time.time() - start_time
                
                if response.status_code != 200:
                    return ModelResponse(
                        model=model,
                        response="",
                        tokens_used=0,
                        prompt_tokens=0,
                        completion_tokens=0,
                        time_taken=time_taken,
                        error=f"API Error: {response.status_code} - {response.text}"
                    )
                
                data = response.json()
                usage = data.get("usage", {})
                choice = data.get("choices", [{}])[0]
                
                return ModelResponse(
                    model=model,
                    response=choice.get("message", {}).get("content", ""),
                    tokens_used=usage.get("total_tokens", 0),
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    time_taken=time_taken,
                    finish_reason=choice.get("finish_reason"),
                    cost=None  # OpenRouter doesn't always provide cost in response
                )
                
        except Exception as e:
            time_taken = time.time() - start_time
            return ModelResponse(
                model=model,
                response="",
                tokens_used=0,
                prompt_tokens=0,
                completion_tokens=0,
                time_taken=time_taken,
                error=f"Exception: {str(e)}"
            )
    
    async def call_models_parallel(
        self,
        models: List[str],
        system_prompt: str,
        user_message: str
    ) -> List[ModelResponse]:
        """
        Call multiple models in parallel
        
        Args:
            models: List of model identifiers
            system_prompt: System prompt to set context
            user_message: User message/question
            
        Returns:
            List of ModelResponse objects
        """
        tasks = [
            self.call_model(model, system_prompt, user_message)
            for model in models
        ]
        
        responses = await asyncio.gather(*tasks)
        return list(responses)
    
    async def get_available_models(self, use_static_list: bool = True) -> List[Dict[str, Any]]:
        """
        Fetch available models from OpenRouter or use static list
        
        Args:
            use_static_list: If True, load from static model_list.json file
        
        Returns:
            List of available models with their metadata
        """
        if use_static_list:
            # Load from static model list file
            model_list_path = Path(__file__).parent.parent.parent / "models" / "model_list.json"
            try:
                if model_list_path.exists():
                    with open(model_list_path, 'r') as f:
                        models = json.load(f)
                        return models
            except Exception as e:
                print(f"Error loading static model list: {e}")
        
        # Fallback to fetching from OpenRouter API
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])
                return []
                
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []


# Create service instance
openrouter_service = OpenRouterService()
