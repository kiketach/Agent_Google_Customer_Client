import logging
import warnings
from google.adk import Agent
from dotenv import load_dotenv
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION

load_dotenv()

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# configure logging __name__
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=configs.agent_settings.model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[]
)