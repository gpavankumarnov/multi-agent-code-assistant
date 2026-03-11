from models.ollama_client import llm

import os
import subprocess


def test_agent(state):

    issue = state["issue"]
    code_patch = state["code_patch"]
    local_repo_path = state["local_repo_path"]

    prompt = f"""
You are a QA engineer.

Issue:
{issue}

Updated Code:
{code_patch}

Write a pytest unit test that validates the fix.

Return ONLY the test code.
"""

    test_code = llm.invoke(prompt)

    test_file = os.path.join(local_repo_path, "test_ai_fix.py")

    with open(test_file, "w") as f:
        f.write(test_code.content)

    result = subprocess.run(
        ["pytest"], cwd=local_repo_path, capture_output=True, text=True
    )

    return {"test_file": test_file, "test_output": result.stdout}


"""
State becomes:

{
 "local_repo_path": "...",
 "issue": "...",
 "code_context": "...",
 "plan": "...",
 "code_patch": "...",
 "test_file": "repo/test_ai_fix.py",
 "test_output": "..."
}
"""
