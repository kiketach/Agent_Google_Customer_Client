
from google.adk.evaluation.agent_evaluator import AgentEvaluator

import os
import pytest
from dotenv import find_dotenv, load_dotenv
from customer_service.config import Config


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(find_dotenv(".env"))
    c = Config()


def test_eval_simple():
    """Test the agent's basic ability via a session file."""
    AgentEvaluator.evaluate(
        "customer_service",
        os.path.join(os.path.dirname(__file__), "eval_data/simple.test.json"),
        num_runs=1,
    )


def test_eval_full_conversation():
    """Test the agent's basic ability via a session file."""
    AgentEvaluator.evaluate(
        "customer_service",
        os.path.join(
            os.path.dirname(__file__), "eval_data/full_conversation.test.json"
        ),
        num_runs=1,
    )
