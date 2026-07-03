"""Competitor research agent built on `deepagents`.

A lead agent plans and delegates to subagents (scout, researchers, fact-checker)
that fan out over the web, then synthesizes a comparison matrix + analysis.

Each run gets its own folder under `runs/<thread_id>/` holding the agent's
files (plan.md, notes.md, findings/) and its checkpoint db, so you can inspect
exactly what happened and resume a crashed run.

Usage:
    python main.py "Analyze the competitors of Notion in the docs space"
    python main.py "Compare Linear against Jira and Asana"
    python main.py --resume <thread_id>   # continue a crashed run
"""

import logging
import os
import sqlite3
import sys
import uuid

from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.sqlite import SqliteSaver

from agents import build_agent

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

RUNS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")


def parse_args(argv):
    """Return (question, resume_thread_id) from CLI args."""
    resume_thread_id = None
    if argv and argv[0] == "--resume":
        if len(argv) < 2:
            sys.exit("usage: python main.py --resume <thread_id>")
        resume_thread_id = argv[1]
        argv = argv[2:]

    question = " ".join(argv) or (
        "Analyze the main competitors of Notion in the productivity and "
        "collaborative-docs space, and where Notion is differentiated vs. exposed."
    )
    return question, resume_thread_id


def main():
    question, resume_thread_id = parse_args(sys.argv[1:])
    thread_id = resume_thread_id or f"competitor-{uuid.uuid4().hex[:12]}"

    run_dir = os.path.join(RUNS_DIR, thread_id)
    os.makedirs(run_dir, exist_ok=True)

    # virtual_mode anchors every agent path under run_dir and blocks traversal.
    backend = FilesystemBackend(root_dir=run_dir, virtual_mode=True)
    # check_same_thread=False: parallel subagents touch the saver from threads.
    conn = sqlite3.connect(
        os.path.join(run_dir, "checkpoints.sqlite"), check_same_thread=False
    )
    agent = build_agent(backend, SqliteSaver(conn))

    logger.info("Competitor research: %s", question)
    logger.info("Run folder: %s", run_dir)
    logger.info("Resume with: python main.py --resume %s", thread_id)

    config = {"configurable": {"thread_id": thread_id}}
    # On resume pass input=None so langgraph continues from the saved checkpoint.
    agent_input = None if resume_thread_id else {
        "messages": [{"role": "user", "content": question}]
    }

    try:
        result = agent.invoke(agent_input, config=config)
        final = result["messages"][-1].content
        print(final if isinstance(final, str) else str(final))
    except Exception:
        logger.exception("Agent run failed")
        logger.error("State is checkpointed -- resume with:\n"
                     "    python main.py --resume %s", thread_id)


if __name__ == "__main__":
    main()
