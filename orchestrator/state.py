from typing import TypedDict, Optional


# State schema for the orchestrator


class AgentState(TypedDict):
    issue: str
    repo_path: str
    code_context: Optional[str]
    plan: Optional[str]
    patch: Optional[str]
    tests: Optional[str]
    pr_url: Optional[str]
