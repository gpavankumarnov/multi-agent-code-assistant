# multi-agent-code-assistant
An AI system that automatically fixes code errors by coordinating multiple agents.

10. Updated End-to-End Flow

Full architecture now:

User enters issue
        ↓
Streamlit UI
        ↓
FastAPI
        ↓
run_agent()
        ↓
Code Reader Agent
        ↓
VectorDB search
        ↓
Relevant code
        ↓
Planner Agent (LLM)
        ↓
Code Writer Agent (LLM)
        ↓
Test Writer Agent
        ↓
PR Agent
        ↓
GitHub Pull Request



11. Where Each Component Lives in Your Project
agents
 ├ code_reader.py
 ├ planner.py
 ├ code_writer.py
 ├ test_writer.py
 └ pr_agent.py

orchestrator
 ├ graph.py
 ├ run_agent.py
 └ state.py

tools
 ├ vector_store.py
 ├ repo_reader.py
 └ github_tools.py

models
 └ ollama_client.py