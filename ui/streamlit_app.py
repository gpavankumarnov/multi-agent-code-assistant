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
    st.write("Running agent...")

    response = requests.post(
        "http://localhost:8000/fix", json={"repo": repo, "issue": issue}
    )
    data = response.json()

    # displaying results
    st.write(data)

    st.subheader("Plan")
    st.write(data["plan"])

    st.subheader("Patch")
    st.code(data["patch"])

    st.subheader("Pull Request")
    st.write(data["pr_url"])
