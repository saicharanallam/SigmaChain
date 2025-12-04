"""
Workflow Orchestrator
Manages the multi-agent pipeline and coordinates agent execution.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from agents.base_agent import BaseAgent, AgentResult
from agents.prompt_enhancer import PromptEnhancerAgent
from agents.image_generator import ImageGeneratorAgent
from agents.validator import ValidationAgent


class WorkflowOrchestrator:
    """
    Orchestrates the agentic workflow pipeline.
    This is the core of the agentic system - it manages agent execution flow.
    """
    
    def __init__(self, model_name: str = "runwayml/stable-diffusion-v1-5"):
        """
        Initialize the workflow orchestrator with agents.
        
        Args:
            model_name: Hugging Face model name for Stable Diffusion
        """
        self.agents: List[BaseAgent] = [
            PromptEnhancerAgent(),
            ImageGeneratorAgent(model_name=model_name),
            ValidationAgent()
        ]
        self.workflow_history: List[Dict[str, Any]] = []
    
    async def execute(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute the complete agentic workflow.
        
        Workflow:
        1. Prompt Enhancement Agent -> enhances the prompt
        2. Image Generation Agent -> generates the image
        3. Validation Agent -> validates the image
        
        Returns:
            Complete workflow result with all agent outputs
        """
        workflow_start = datetime.now()
        workflow_data = {
            "user_prompt": user_prompt,
            "workflow_id": f"workflow_{workflow_start.timestamp()}",
            "started_at": workflow_start.isoformat(),
            "steps": []
        }
        
        # Initial input data
        current_data = {"prompt": user_prompt}
        
        try:
            # Step 1: Prompt Enhancement
            enhancer_result = await self.agents[0].process(current_data)
            workflow_data["steps"].append({
                "agent": self.agents[0].name,
                "status": "success" if enhancer_result.success else "failed",
                "result": enhancer_result.dict(),
                "timestamp": datetime.now().isoformat()
            })
            
            if not enhancer_result.success:
                workflow_data["status"] = "failed"
                workflow_data["error"] = enhancer_result.message
                return workflow_data
            
            # Merge enhanced prompt data
            current_data.update(enhancer_result.data)
            
            # Step 2: Image Generation
            generator_result = await self.agents[1].process(current_data)
            workflow_data["steps"].append({
                "agent": self.agents[1].name,
                "status": "success" if generator_result.success else "failed",
                "result": generator_result.dict(),
                "timestamp": datetime.now().isoformat()
            })
            
            if not generator_result.success:
                workflow_data["status"] = "failed"
                workflow_data["error"] = generator_result.message
                return workflow_data
            
            # Merge image data
            current_data.update(generator_result.data)
            
            # Step 3: Validation
            validator_result = await self.agents[2].process(current_data)
            workflow_data["steps"].append({
                "agent": self.agents[2].name,
                "status": "success" if validator_result.success else "failed",
                "result": validator_result.dict(),
                "timestamp": datetime.now().isoformat()
            })
            
            # Final workflow result
            workflow_data["status"] = "completed"
            workflow_data["completed_at"] = datetime.now().isoformat()
            workflow_data["duration_seconds"] = (datetime.now() - workflow_start).total_seconds()
            workflow_data["final_result"] = {
                "original_prompt": user_prompt,
                "enhanced_prompt": current_data.get("enhanced_prompt"),
                "image_url": current_data.get("image_url"),
                "validation": current_data.get("validation"),
                "passed_validation": validator_result.data.get("passed", False) if validator_result.success else None
            }
            
            # Store in history
            self.workflow_history.append(workflow_data)
            
            return workflow_data
            
        except Exception as e:
            workflow_data["status"] = "error"
            workflow_data["error"] = str(e)
            workflow_data["completed_at"] = datetime.now().isoformat()
            return workflow_data
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.workflow_history[-limit:]
    
    def add_agent(self, agent: BaseAgent, position: Optional[int] = None):
        """
        Add a new agent to the workflow.
        This demonstrates extensibility of the agentic system.
        
        Args:
            agent: Agent instance to add
            position: Position in pipeline (None = append to end)
        """
        if position is None:
            self.agents.append(agent)
        else:
            self.agents.insert(position, agent)

