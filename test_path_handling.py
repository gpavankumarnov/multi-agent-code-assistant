#!/usr/bin/env python3
"""Test path handling in file_editor.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from tools.file_editor import apply_patch

# Test cases
test_cases = [
    {
        "name": "Path with cloned_repos prefix",
        "repo_path": "./cloned_repos/15fdd069-3323-49cc-9198-123a3d28bd19",
        "file_path": "./cloned_repos/15fdd069-3323-49cc-9198-123a3d28bd19/api/weather_service.py",
        "expected": "api/weather_service.py",
    },
    {
        "name": "Relative path",
        "repo_path": "./cloned_repos/uuid",
        "file_path": "api/weather_service.py",
        "expected": "api/weather_service.py",
    },
    {
        "name": "Path with leading ./",
        "repo_path": "./cloned_repos/uuid",
        "file_path": "./api/weather_service.py",
        "expected": "api/weather_service.py",
    },
]

print("=" * 60)
print("Testing Path Handling")
print("=" * 60)

for test in test_cases:
    print(f"\nTest: {test['name']}")
    print(f"Input path: {test['file_path']}")

    file_path = test["file_path"]
    repo_path = test["repo_path"]

    # Simulate the path processing logic
    if os.path.isabs(file_path) and repo_path in file_path:
        file_path = os.path.relpath(file_path, repo_path)

    file_path = file_path.lstrip("./")

    if "cloned_repos/" in file_path:
        parts = file_path.split("cloned_repos/")
        if len(parts) > 1:
            remaining = parts[1]
            if "/" in remaining:
                file_path = "/".join(remaining.split("/")[1:])

    print(f"Processed path: {file_path}")
    print(f"Expected: {test['expected']}")
    print(f"✓ PASS" if file_path == test["expected"] else f"✗ FAIL")

print("\n" + "=" * 60)
