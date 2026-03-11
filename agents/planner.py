from models.ollama_client import llm


def planner_agent(state):

    issue = state["issue"]
    code_context = state["code_context"]

    prompt = f"""
    You are a senior engineer.

Issue:
{issue}

Relevant Code:
{code_context}

Create a step-by-step plan to fix this issue.
"""

    plan = llm.invoke(prompt)

    return {"plan": plan}
