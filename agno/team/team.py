"""
Team module for the Agno framework
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Team(BaseModel):
    """Team class for coordinating multiple agents"""
    
    name: str
    mode: str
    model: Any
    members: List[Any]
    tools: List[Any]
    instructions: List[str]
    markdown: bool = True
    show_members_responses: bool = False
    enable_agentic_context: bool = True
    add_datetime_to_instructions: bool = False
    success_criteria: Optional[str] = None
    
    def print_response(self, prompt: str, stream: bool = True, show_full_reasoning: bool = False, stream_intermediate_steps: bool = False) -> str:
        """Print the team's response to a prompt"""
        # This is a simplified version - in a real implementation, this would coordinate the agents
        response = f"Response from {self.name} team to: {prompt}"
        print(response)
        return response 