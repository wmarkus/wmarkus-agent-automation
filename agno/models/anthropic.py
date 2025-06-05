"""
Anthropic models for the Agno framework
"""

from pydantic import BaseModel

class Claude(BaseModel):
    """Claude model from Anthropic"""
    
    id: str
    
    def __init__(self, id: str):
        super().__init__(id=id) 