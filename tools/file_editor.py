import os


def apply_patch(repo_path, patch):

    file_path = patch["file_path"]
    updated_content = patch["updated_code"]

    # If file_path is absolute and contains the repo_path, make it relative
    if os.path.isabs(file_path) and repo_path in file_path:
        # Extract relative path
        file_path = os.path.relpath(file_path, repo_path)

    # Remove leading ./ if present
    file_path = file_path.lstrip("./")

    # If path contains cloned_repos, extract just the file part after the UUID
    if "cloned_repos/" in file_path:
        # Split by cloned_repos/ and get everything after the UUID directory
        parts = file_path.split("cloned_repos/")
        if len(parts) > 1:
            # Get everything after the UUID (e.g., "uuid/api/file.py" -> "api/file.py")
            remaining = parts[1]
            if "/" in remaining:
                file_path = "/".join(remaining.split("/")[1:])

    full_path = os.path.join(repo_path, file_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w") as f:
        f.write(updated_content)

    return full_path
