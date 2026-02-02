from langgraph.graph import StateGraph, END
from autosec.agent.state import AgentState
from autosec.agent.nodes.planner import planner_node
from autosec.agent.nodes.coder import coder_node
from autosec.agent.nodes.reflector import reflector_node
from autosec.tools.sast_analyzer import analyze_security

def test_node(state: AgentState) -> dict:
    print("--- SAST VERIFICATION ---")
    
    patch = state.get("current_patch", "")
    if not patch:
        return {"test_results": "FAIL: No patch generated", "sast_issues": []}
    
    is_safe, issues = analyze_security(patch)
    
    if is_safe:
        return {"test_results": "TEST PASS: SAST verification clean", "sast_issues": []}
    else:
        return {
            "test_results": f"FAIL: {len(issues)} security issues found",
            "sast_issues": issues
        }

def should_continue(state: AgentState):
    results = state.get("test_results", "")
    iterations = state.get("iterations", 0)
    
    if iterations >= 5:
        return "end"
    if "TEST PASS" in results:
        return "end"
    return "reflect"

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("test", test_node)
    workflow.add_node("reflector", reflector_node)
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "test")
    
    workflow.add_conditional_edges(
        "test",
        should_continue,
        {"end": END, "reflect": "reflector"}
    )
    
    workflow.add_edge("reflector", "coder")
    
    return workflow.compile()
