"""
- creates a multi-agent workflow
- it builds a pipeline of AI agents
  that process a task step-by-step
  using state object
  that flow through the system

"""


def build_graph():

    # create a state graph
    workflow = StateGraph(AgentState)

    # add nodes to the graph
    workflow.add_node("reader", code_reader_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("writer", code_writer_agent)
    workflow.add_node("tester", test_writer_agent)
    workflow.add_node("pr", pr_agent)

    # set entry point
    workflow.set_entry_point("reader")

    # add edges
    workflow.add_edge("reader", "planner")
    workflow.add_edge("planner", "writer")
    workflow.add_edge("writer", "tester")
    workflow.add_edge("tester", "pr")

    return workflow.compile()
