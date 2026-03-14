import json
import re
from models.ollama_client import llm
from tools.file_editor import apply_patch


def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON from surrounding text
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            json_str = match.group()

            # Check if JSON contains Python code like "\n".join([...])
            # This is invalid JSON, so we need to reject it
            if '"\n".join(' in json_str or "'.join(" in json_str:
                raise ValueError(
                    f"LLM returned Python code instead of JSON. "
                    f"The response contains '.join()' which is not valid JSON.\n"
                    f"Response: {text[:500]}"
                )

            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Extracted text looks like JSON but failed to parse: {e}\n"
                    f"Extracted: {json_str[:200]}"
                )

        raise ValueError(f"No valid JSON found in LLM output:\n{text[:500]}")


def clean_code_string(code: str):
    """
    Remove triple quotes if LLM used them.
    """
    if code.startswith('"""') and code.endswith('"""'):
        code = code[3:-3]

    if code.startswith("'''") and code.endswith("'''"):
        code = code[3:-3]

    return code.strip()


def code_writer_agent(state):

    print("\n========== CODE WRITER AGENT ==========\n")

    print("\nSTATE IN WRITER\n")
    print("Issue:", state.get("issue"))
    print("Plan:", state.get("plan"))
    print("Code Context:", state.get("code_context"))

    issue = state["issue"]
    plan = state["plan"]
    code_context = state["code_context"]

    # First, ask LLM to identify the file and generate the fix
    prompt = f"""
You are a senior software engineer fixing a bug.

Issue:
{issue}

Fix Plan:
{plan}

Existing Code:
{code_context}

Instructions:
1. Identify which file needs to be fixed from the "Existing Code" section
2. Write the COMPLETE fixed file content
3. Format your response EXACTLY like this:

FILE_PATH: relative/path/to/file.py
CODE_START
[complete fixed code here]
CODE_END

Example:
FILE_PATH: api/weather_service.py
CODE_START
import requests

class WeatherService:
    def __init__(self):
        pass
CODE_END
"""

    response = llm.invoke(prompt)

    print("\n--- LLM RESPONSE (length: {}) ---\n".format(len(response)))
    print(response[:800])  # Print first 800 chars
    if len(response) > 800:
        print(f"\n... (truncated for display, {len(response) - 800} more chars)")

    # Debug: Check if CODE_END exists
    has_code_start = "CODE_START" in response
    has_code_end = "CODE_END" in response
    print(
        f"\nDEBUG: CODE_START present: {has_code_start}, CODE_END present: {has_code_end}"
    )

    if has_code_start and not has_code_end:
        print(f"\n⚠️  WARNING: LLM response is ACTUALLY truncated by the model")
        print(f"Last 300 chars of response:\n...{response[-300:]}")

    # Parse the structured response
    try:
        # Extract file path
        file_path_match = re.search(r"FILE_PATH:\s*(.+)", response)
        if not file_path_match:
            print(f"\n ERROR: Could not find FILE_PATH in response")
            print(f"Full response:\n{response}")
            raise ValueError("Could not find FILE_PATH in response")

        file_path = file_path_match.group(1).strip()
        print(f"\n Extracted file_path: {file_path}")

        # Extract code between CODE_START and CODE_END
        code_match = re.search(r"CODE_START\s*\n(.*?)\nCODE_END", response, re.DOTALL)

        if not code_match:
            # Check if CODE_START exists but CODE_END is missing (truncated response)
            if "CODE_START" in response and "CODE_END" not in response:
                print(
                    f"\n⚠️  WARNING: LLM response truncated - using fallback extraction"
                )
                print(f"Response length: {len(response)} chars")

                # Fallback: Extract everything after CODE_START
                fallback_match = re.search(r"CODE_START\s*\n(.*)", response, re.DOTALL)
                if fallback_match:
                    updated_code = fallback_match.group(1).strip()
                    print(
                        f"✓ Extracted {len(updated_code)} chars using fallback method"
                    )
                    print(f"⚠️  Note: This may be incomplete due to model token limits")
                else:
                    raise ValueError("Could not extract code even with fallback method")
            else:
                print(f"\n❌ ERROR: Could not find CODE_START...CODE_END markers")
                print(f"Full response:\n{response}")
                raise ValueError("Could not find CODE_START...CODE_END in response")
        else:
            updated_code = code_match.group(1)
        print(f"\n Extracted code ({len(updated_code)} chars)")

        # Clean up file path - remove cloned_repos prefix if present
        if "cloned_repos/" in file_path:
            parts = file_path.split("cloned_repos/")
            if len(parts) > 1:
                remaining = parts[1]
                if "/" in remaining:
                    file_path = "/".join(remaining.split("/")[1:])

        file_path = file_path.lstrip("./")
        print(f"\n Cleaned file_path: {file_path}")

        patch = {"file_path": file_path, "updated_code": updated_code}

    except Exception as e:
        print(f"\n FATAL: Failed to parse LLM response: {e}")
        raise

    # Validate structure
    if "file_path" not in patch or "updated_code" not in patch:
        raise ValueError(f"Invalid patch format: {patch}")

    # Clean code string
    patch["updated_code"] = clean_code_string(patch["updated_code"])

    print("\n--- PARSED PATCH ---\n")
    print(patch)

    # Apply patch to repo
    apply_patch(state["local_repo_path"], patch)

    print("\nPatch successfully applied.\n")
    print("✅ Writer Agent - Completed")

    return {"patch": patch}
