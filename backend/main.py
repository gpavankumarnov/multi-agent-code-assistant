from fastapi import FastAPI
from pydantic import BaseModel
from services.repo_service import resolve_repo
from orchestrator.run_Agent import run_agent
import sys
from io import StringIO

app = FastAPI()


# This model is typically used to validate the payload of an HTTP request (e.g., in a POST request to create an issue).
# The model definition
class IssueRequest(BaseModel):
    repo: str
    issue: str


# The repo should be cloned before calling run_agent(), and the local clone path should be passed into the agent state.


@app.post("/fix")
def create_issue(request: IssueRequest):
    # Capture stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = sys.stderr = log_capture = StringIO()

    try:
        repo_url = request.repo
        try:
            # resolve repo (clone or use local path)
            local_repo_path = resolve_repo(repo_url)
        except Exception:
            raise

        # call langgraph workflow
        result = run_agent(
            local_repo_path=local_repo_path, issue=request.issue, repo_url=repo_url
        )

        # Add captured logs to result
        result["logs"] = log_capture.getvalue()

        return result
    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        # Also print logs to console
        print(log_capture.getvalue(), end="")


# If a client sends JSON data without a repo or issue, or with the wrong type (e.g., an integer), Pydantic will automatically raise a validation error.
