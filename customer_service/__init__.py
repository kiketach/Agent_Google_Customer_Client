"""Customer Service Agent package."""
from .agent import root_agent
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION

__all__ = ['root_agent', 'Config', 'GLOBAL_INSTRUCTION', 'INSTRUCTION']
