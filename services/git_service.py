import os  # file operations
import subprocess  # git operations
import uuid


"""

What this does

Creates a folder ./cloned_repos

Generates a unique repo folder

Runs:

git clone <repo_url> <clone_path>

Returns the local path

Example result:

./cloned_repos/92c41e4c-8c63-4b61-8b2f

"""


def clone_repo(repo_url: str, base_dir="./cloned_repos") -> str:
    os.makedirs(base_dir, exist_ok=True)

    repo_id = str(uuid.uuid4())
    clone_path = os.path.join(base_dir, repo_id)

    subprocess.run(["git", "clone", repo_url, clone_path], check=True)
    return clone_path
