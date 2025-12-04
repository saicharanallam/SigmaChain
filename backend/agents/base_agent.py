"""
Base Agent class for all agents in the workflow.
This demonstrates the agentic pattern where each agent has a specific role.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentResult(BaseModel):
    """Standard result format for all agents"""
    success: bool
    data: Dict[str, Any]
    message: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base class for all agents in the agentic workflow.
    Each agent processes input and produces output that flows to the next agent.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Process input data and return result.
        This is where each agent's specific logic is implemented.
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"

