from orchestrator.graph import build_graph
from orchestrator.state import AgentState


def run_agent(repo_path: str, issue: str):

    # call build_graph func
    graph = build_graph()

    initial_state: AgentState = {
        "repo_path": repo_path,
        "issue": issue,
        "code_context": None,
        "plan": None,
        "patch": None,
        "tests": None,
        "pr_url": None,
    }

    # invoke the graph with initial state
    # langgraph looks for the node you designated as the START
    # it hands that node it with the initial state
    result = graph.invoke(initial_state)
    return {
        "plan": result["plan"],
        "patch": result["patch"],
        "pr_url": result["pr_url"],
    }
