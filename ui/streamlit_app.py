import streamlit as st
import requests


st.title("AI Developer Agent")


# create inputs to receive from user

repo = st.text_input("Repository URL")

issue = st.text_area("Describe the issue")


# When user click submit button
# - call the backend API
# - display the results


if st.button("Run Agent"):
    # Create placeholders for each stage
    clone_status = st.empty()
    reader_status = st.empty()
    planner_status = st.empty()
    writer_status = st.empty()
    tester_status = st.empty()
    pr_status = st.empty()

    # Show initial loading states
    clone_status.markdown("⏳ **Cloning repository...**")
    reader_status.markdown("⏸️ Reader Agent")
    planner_status.markdown("⏸️ Planner Agent")
    writer_status.markdown("⏸️ Writer Agent")
    tester_status.markdown("⏸️ Tester Agent")
    pr_status.markdown("⏸️ PR Agent")

    # Make API call
    response = requests.post(
        "http://localhost:8000/fix", json={"repo": repo, "issue": issue}
    )
    data = response.json()

    # Parse logs to update stages based on completion messages
    logs = data.get("logs", "")

    # Update stages based on what's in the logs
    if "Repository cloned" in logs or "✓" in logs:
        clone_status.markdown("✅ **Repository cloned**")

    if "Reader Agent - Completed" in logs:
        reader_status.markdown("✅ **Reader Agent - Completed**")

    if "Planner Agent - Completed" in logs:
        planner_status.markdown("✅ **Planner Agent - Completed**")

    if "Writer Agent - Completed" in logs:
        writer_status.markdown("✅ **Writer Agent - Completed**")

    if "Tester Agent - Completed" in logs:
        tester_status.markdown("✅ **Tester Agent - Completed**")

    if "PR Agent - Completed" in logs:
        pr_status.markdown("✅ **PR Agent - Completed**")

    # Display Vector DB search results
    st.markdown("---")
    st.subheader("🔍 Vector DB Search Results")
    vector_results = data.get("vector_db_results", "No results available")
    st.text(vector_results)
