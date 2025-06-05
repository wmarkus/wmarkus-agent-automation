"""
Agent module for the Agno framework
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Agent(BaseModel):
    """Base Agent class for the Agno framework"""
    
    name: str
    role: str
    model: Any
    tools: List[Any]
    instructions: List[str]
    add_datetime_to_instructions: bool = False
    
    def print_response(self, prompt: str, stream: bool = True, show_full_reasoning: bool = False, stream_intermediate_steps: bool = False) -> str:
        """Print the agent's response to a prompt"""
        # This is a simplified version - in a real implementation, this would use the model to generate a response
        response = f"Response from {self.name} to: {prompt}"
        print(response)
        return response 