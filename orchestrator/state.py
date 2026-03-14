from typing import TypedDict, Optional


# State schema for the orchestrator


class AgentState(TypedDict):
    issue: str
    local_repo_path: str
    repo_url: str
    code_context: Optional[str]
    vector_db_results: Optional[str]
    plan: Optional[str]
    patch: Optional[str]
    tests: Optional[str]
    test_output: Optional[str]
    pr_url: Optional[str]
