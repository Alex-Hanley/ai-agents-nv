"""Web search tool (the workers' primary tool) and a tool-call logger."""

import logging
import os
from typing import Literal

from dotenv import load_dotenv
from langchain.agents.middleware import wrap_tool_call
from tavily import TavilyClient

load_dotenv()

logger = logging.getLogger(__name__)

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search and return results (title, url, content snippet).

    Use specific, narrow queries. For pricing or funding, prefer the
    competitor's own domain or `topic="finance"`.
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


@wrap_tool_call
def log_tool_calls(request, handler):
    tool_call = getattr(request, "tool_call", None)
    if isinstance(tool_call, dict):
        tool_name = tool_call.get("name", "tool")
        tool_args = tool_call.get("args")
    else:
        tool_name = getattr(request, "name", "tool")
        tool_args = getattr(request, "args", None)

    if tool_args:
        summary = str(tool_args)
        if len(summary) > 200:
            summary = summary[:199] + "…"
        logger.info("→ %s(%s)", tool_name, summary)
    else:
        logger.info("→ %s", tool_name)
    return handler(request)
