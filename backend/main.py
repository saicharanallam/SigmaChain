"""
FastAPI backend for the agentic image generation system.
"""

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from workflow.orchestrator import WorkflowOrchestrator

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SigmaChain - Agentic Image Generation",
    description="Multi-agent system for intelligent image generation and validation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create generated_images directory if it doesn't exist
generated_images_dir = Path("generated_images")
generated_images_dir.mkdir(parents=True, exist_ok=True)

# Mount static files for serving generated images
app.mount("/static/images", StaticFiles(directory=str(generated_images_dir)), name="static_images")

# Initialize orchestrator
orchestrator = WorkflowOrchestrator()


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    success: bool
    workflow_id: str
    result: dict
    message: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SigmaChain Agentic Image Generation",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    """
    Main endpoint for image generation workflow.
    This triggers the complete agentic pipeline.
    """
    try:
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Execute workflow
        workflow_result = await orchestrator.execute(
            user_prompt=request.prompt
        )
        
        if workflow_result["status"] == "completed":
            return GenerateResponse(
                success=True,
                workflow_id=workflow_result["workflow_id"],
                result=workflow_result["final_result"],
                message="Image generated and validated successfully"
            )
        else:
            return GenerateResponse(
                success=False,
                workflow_id=workflow_result.get("workflow_id", "unknown"),
                result=workflow_result,
                message=workflow_result.get("error", "Workflow failed")
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_history(limit: int = 10):
    """Get workflow execution history"""
    return {
        "history": orchestrator.get_history(limit=limit)
    }


@app.get("/api/workflow/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get specific workflow result by ID"""
    history = orchestrator.get_history(limit=100)
    for workflow in history:
        if workflow["workflow_id"] == workflow_id:
            return workflow
    raise HTTPException(status_code=404, detail="Workflow not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

