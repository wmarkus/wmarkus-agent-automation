"""
WMarkus Agent Universe - Main Entry Point

This module serves as the main entry point for the WMarkus Agent Universe framework.
It provides the core functionality for initializing and managing agents.
"""

import os
from typing import Dict, List, Optional

from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgentUniverse:
    """Main class for managing the agent universe."""
    
    def __init__(self):
        """Initialize the Agent Universe."""
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.agents: Dict[str, "BaseAgent"] = {}
        
    def register_agent(self, agent: "BaseAgent") -> None:
        """Register a new agent in the universe.
        
        Args:
            agent: The agent instance to register
        """
        self.agents[agent.name] = agent
        
    def get_agent(self, name: str) -> Optional["BaseAgent"]:
        """Get an agent by name.
        
        Args:
            name: The name of the agent to retrieve
            
        Returns:
            The agent instance if found, None otherwise
        """
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """List all registered agent names.
        
        Returns:
            List of agent names
        """
        return list(self.agents.keys())

def main():
    """Main entry point for the application."""
    universe = AgentUniverse()
    print("WMarkus Agent Universe initialized!")
    print("Ready to register and manage agents.")

if __name__ == "__main__":
    main()
