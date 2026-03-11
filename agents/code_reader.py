"""
Code Reader Agent Using VectorDB

Your Code Reader agent should now do:

1️⃣ ensure repo indexed
2️⃣ search VectorDB
3️⃣ return relevant code
VectorDB is used only by the Code Reader agent.

User Issue
   ↓
FastAPI
   ↓
run_agent()
   ↓
Code Reader Agent
   ↓
VectorDB Retrieval
   ↓
Relevant Code Files
   ↓
Planner Agent (LLM)
"""

from tools.vector_store import index_repository, search_code


def code_reader_agent(state):

    local_repo_path = state["local_repo_path"]
    issue = state["issue"]

    # index repository
    # extracts all .py files and creates embeddings
    index_repository(local_repo_path)

    # search relevant files
    relevant_files = search_code(issue)

    context = "\n\n".join(relevant_files)

    return {"code_context": context}

    # Now the next agents receive only relevant code context.


"""

3. How LangGraph Updates the State

Internally LangGraph does something like:

state.update(agent_output)

So after the reader runs:

Before reader
{
  "repo_path": "/repo/project",
  "issue": "authentication failing"
}
Reader returns
{
  "code_context": "def login(): ..."
}
LangGraph merges it
{
  "repo_path": "/repo/project",
  "issue": "authentication failing",
  "code_context": "def login(): ..."
}

The original state is preserved.



4. What the Next Agent Receives

Now the planner agent gets the updated state:

def planner_agent(state):

    context = state["code_context"]
    issue = state["issue"]

State now looks like:

{
  "repo_path": "/repo/project",
  "issue": "authentication failing",
  "code_context": "def login(): ..."
}

So the planner can use the context retrieved by the reader.
"""
