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

    # Create a summary of what vector DB returned
    vector_db_summary = (
        f"Vector DB found {len(relevant_files)} relevant file(s) for the issue:\n"
    )
    for i, file_content in enumerate(relevant_files, 1):
        # Extract file path from the content (format: "File: /path/to/file.py\n\ncode...")
        if file_content.startswith("File: "):
            file_path = file_content.split("\n")[0].replace("File: ", "")
            vector_db_summary += f"{i}. {file_path}\n"

    print(f"\n{vector_db_summary}")
    print("✅ Reader Agent - Completed")
    return {"code_context": context, "vector_db_results": vector_db_summary}

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
