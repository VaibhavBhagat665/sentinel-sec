from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from autosec.agent.state import AgentState
from autosec.agent.llm import get_llm

llm = get_llm(temperature=0)

REFLECTOR_PROMPT = """You are a code reviewer analyzing a failed security patch.

Given the patch code and SAST output, provide:
1. Root cause of failure
2. Specific fix instructions

Be concise. Do not write code."""

def reflector_node(state: AgentState) -> Dict[str, Any]:
    print("--- REFLECTOR NODE ---")
    
    patch = state.get('current_patch', "")
    test_results = state.get('test_results', "")
    sast_issues = state.get('sast_issues', [])
    
    issues_str = "\n".join(sast_issues) if sast_issues else "None"
    
    response = llm.invoke([
        SystemMessage(content=REFLECTOR_PROMPT),
        HumanMessage(content=f"Patch:\n{patch}\n\nTest Output: {test_results}\n\nSAST Issues:\n{issues_str}")
    ])
    
    return {
        "messages": [response],
        "error_analysis": response.content
    }
