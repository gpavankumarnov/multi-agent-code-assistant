import os
from services.git_service import clone_repo


def resolve_repo(repo_input: str):
    if (
        repo_input.startswith("http://")
        or repo_input.startswith("https://")
        or repo_input.startswith("git@")
    ):
        return clone_repo(repo_input)
    # assume local path
    if os.path.exists(repo_input):
        return repo_input

    raise ValueError("Invalid repository path or URL")


"""
4. Example Flow

User sends:

{
 "repo_url": "https://github.com/user/project.git",
 "issue": "login failing"
}

Backend clones repo:

repo_path = clone_repository(repo_url)

Now state becomes:

{
 "repo_url": "https://github.com/user/project.git",
 "repo_path": "./cloned_repos/123",
 "issue": "login failing"
}
"""
