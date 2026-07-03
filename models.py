"""Per-role LLM routing on Nebius Token Factory.

The lead does planning + synthesis (reasoning quality matters most); the workers
fan out in parallel, so they get a cheaper/faster model that scales with fan-out.
"""

import os

from dotenv import load_dotenv
from langchain_nebius import ChatNebius

load_dotenv()

LEAD_MODEL_NAME = os.environ.get("LEAD_MODEL", "MiniMaxAI/MiniMax-M2.5")
WORKER_MODEL_NAME = os.environ.get("WORKER_MODEL", "MiniMaxAI/MiniMax-M2.5")

LEAD_MODEL = ChatNebius(
    model=LEAD_MODEL_NAME,
    temperature=0.3,
    timeout=120,
    max_retries=2,
    reasoning_effort="high",
)

WORKER_MODEL = ChatNebius(
    model=WORKER_MODEL_NAME,
    temperature=0.2,
    timeout=120,
    max_retries=2,
    reasoning_effort="medium",
)
