We are making a course about how to create agents in Python and specifically in this course we are going to show competitors research agents this agent should be based on library in deep agents. We will use Tavily for web search and Nebius Token Factory for LLM APIs

## Local environment

A local virtual environment lives in `.venv` (Python 3.13). Always use it when running or installing anything — do not use the system Python.

Setup (already done, only needed on a fresh clone):

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Running commands — always go through the venv, e.g.:

```bash
.venv/bin/python main.py
.venv/bin/python -m pip install <package>
```

Or activate it first: `source .venv/bin/activate`.

Copy `.env.example` to `.env` and fill in `NEBIUS_API_KEY` and `TAVILY_API_KEY` before running.
