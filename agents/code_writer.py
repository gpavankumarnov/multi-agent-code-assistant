import json
from models.ollama_client import llm
from tools.file_editor import apply_patch


def code_writer_agent(state):

    issue = state["issue"]
    plan = state["plan"]
    code_context = state["code_context"]

    prompt = f"""
You are a senior software engineer.

Issue:
{issue}

Fix Plan:
{plan}

Existing Code:
{code_context}

Return the fix in JSON format:

{{
  "file_path": "relative/path/to/file.py",
  "updated_code": "full updated code"
}}
"""

    response = llm.invoke(prompt)

    patch = json.loads(response)

    apply_patch(state["local_repo_path"], patch)

    return {"code_patch": patch}


"""

Now state becomes:

{
 "issue": "...",
 "code_context": "...",
 "plan": "...",
 "code_patch": {
      "file_path": "service/auth.py",
      "updated_code": "..."
 }
}

"""
