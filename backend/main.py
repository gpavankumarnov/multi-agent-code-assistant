from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# This model is typically used to validate the payload of an HTTP request (e.g., in a POST request to create an issue).
# The model definition
class IssueRequest(BaseModel):
    repo: str
    issue: str


@app.post("/create-issue")
def create_issue(request: IssueRequest):
    # call langgraph workflow
    # result = run_agent(repo=request.repo, issue=request.issue)

    return {"message": "Issue created successfully"}


# If a client sends JSON data without a repo or issue, or with the wrong type (e.g., an integer), Pydantic will automatically raise a validation error.
