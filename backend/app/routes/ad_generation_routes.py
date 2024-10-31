from fastapi import APIRouter, HTTPException, UploadFile, Depends, Query
from typing import List, Dict
from app.utils.prompt_construction import PromptOptimizer, split_prompt  # Ensure correct import based on file structure
from app.schemas import PromptRequest, OptimizedPromptRequest

# Initialize the optimizer instance
optimizer = PromptOptimizer()
ad_generation_router = APIRouter()

@ad_generation_router.post("/process_prompt/", response_model=Dict[str, str])
async def process_prompt(prompt: str = Query(..., description="The raw user prompt to process")):
    """
    Process a prompt to generate optimized ad variations for different marketing goals.
    
    Parameters:
    - prompt_data: Contains the prompt text to be processed
    
    Returns:
    - Dict[str, str]: A dictionary with optimized prompt variations for each category goal
    """
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
        
    try:
        result = await optimizer.analyze_prompt(prompt.strip())
        
        if not result or "error" in result:
            raise HTTPException(status_code=500, detail="Failed to process prompt")

        return result
    except Exception as e:
        print(f"Error processing prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
@ad_generation_router.post("/optimizedprompt/")
async def optimized_prompt(request: OptimizedPromptRequest):
    """
    Generates specialized prompts for image, video, and ad copy for each category.
    """
    try:
        if request.image:
            image_content = await request.image.read()  # Process image if required
            # You can add any image handling logic here, e.g., saving or processing

        # Pass the optimized prompts to the split_prompt function
        optimized_prompts = await split_prompt(request.prompt)
        
        if "error" in optimized_prompts:
            raise HTTPException(status_code=500, detail="Failed to generate specialized prompts")

        return optimized_prompts
    except Exception as e:
        print(f"Error in optimized prompt generation: {e}")
        raise HTTPException(status_code=400, detail="Error processing optimized prompts")
