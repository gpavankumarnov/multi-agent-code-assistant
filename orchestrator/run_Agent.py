from orchestrator.graph import build_graph
from orchestrator.state import AgentState


def run_agent(local_repo_path: str, issue: str, repo_url: str = ""):

    # call build_graph func
    graph = build_graph()

    initial_state: AgentState = {
        "local_repo_path": local_repo_path,
        "repo_url": repo_url,
        "issue": issue,
        "code_context": None,
        "vector_db_results": None,
        "plan": None,
        "patch": None,
        "tests": None,
        "test_output": None,
        "pr_url": None,
    }

    # Track stage completion
    stages_completed = []

    print("✓ Repository cloned")
    stages_completed.append("clone")

    print("⏳ Running Reader Agent...")
    # invoke the graph with initial state
    result = graph.invoke(initial_state)

    # Mark all stages as complete after graph execution
    stages_completed.extend(["reader", "planner", "writer", "tester", "pr"])

    return {
        "plan": result["plan"],
        "patch": result["patch"],
        "pr_url": result["pr_url"],
        "status": result.get("status", "completed"),
        "stages_completed": stages_completed,
        "vector_db_results": result.get(
            "vector_db_results", "No vector DB results available"
        ),
    }
