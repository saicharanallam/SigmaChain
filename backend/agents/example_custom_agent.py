"""
Example Custom Agent
This demonstrates how to create a new agent for the workflow.
You can add this agent to extend the workflow with new capabilities.
"""

from typing import Dict, Any
from .base_agent import BaseAgent, AgentResult


class ExampleCustomAgent(BaseAgent):
    """
    Example agent that demonstrates how to create custom agents.
    This agent could be used for:
    - Image post-processing
    - Style transfer
    - Background removal
    - Image upscaling
    - etc.
    """
    
    def __init__(self):
        super().__init__(
            name="ExampleCustomAgent",
            description="Example custom agent for demonstration"
        )
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Process input data and return result.
        This is where your custom agent logic goes.
        """
        try:
            # Get input data
            image_url = input_data.get("image_url", "")
            
            if not image_url:
                return AgentResult(
                    success=False,
                    data={},
                    message="No image URL provided"
                )
            
            # Your custom processing logic here
            # For example:
            # - Call an API
            # - Process the image
            # - Apply transformations
            # - etc.
            
            # Example: Just pass through the data with modification
            processed_data = {
                "image_url": image_url,
                "processed": True,
                "custom_field": "custom_value"
            }
            
            return AgentResult(
                success=True,
                data=processed_data,
                message="Custom agent processing completed",
                metadata={
                    "agent_type": "custom",
                    "processing_time": 0.5
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                data={},
                message=f"Error in custom agent: {str(e)}"
            )


# To add this agent to the workflow, modify workflow/orchestrator.py:
# 
# from agents.example_custom_agent import ExampleCustomAgent
# 
# class WorkflowOrchestrator:
#     def __init__(self):
#         self.agents = [
#             PromptEnhancerAgent(),
#             ImageGeneratorAgent(),
#             ExampleCustomAgent(),  # Add your custom agent here
#             ValidationAgent()
#         ]

