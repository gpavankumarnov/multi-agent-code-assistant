import os


def apply_patch(repo_path, patch):

    file_path = patch["file_path"]
    updated_content = patch["updated_code"]

    full_path = os.path.join(repo_path, file_path)

    with open(full_path, "w") as f:
        f.write(updated_content)

    return full_path
