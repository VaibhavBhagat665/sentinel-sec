from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from autosec.agent.state import AgentState
from autosec.agent.llm import get_llm

llm = get_llm(temperature=0)

CODER_PROMPT = """You are a Python security engineer. Implement the fix from the plan.

Rules:
- Return ONLY the fixed function code
- Use parameterized queries for SQL
- Use subprocess with shell=False for commands
- Validate all user input

Return code in ```python blocks."""

def coder_node(state: AgentState) -> Dict[str, Any]:
    print("--- CODER NODE ---")
    
    messages = state['messages']
    last_message = messages[-1]
    cve_id = state['cve_id']
    error_analysis = state.get('error_analysis')
    sast_issues = state.get('sast_issues', [])
    
    if error_analysis or sast_issues:
        issues_str = "\n".join(sast_issues) if sast_issues else ""
        prompt = f"CVE: {cve_id}\nPREVIOUS CODE FAILED.\nFeedback: {error_analysis}\nSAST Issues:\n{issues_str}\n\nFix the code."
    else:
        prompt = f"CVE: {cve_id}\nPlan: {last_message.content}\n\nImplement the fix."

    response = llm.invoke([
        SystemMessage(content=CODER_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    content = response.content
    code_block = content
    
    if "```python" in content:
        code_block = content.split("```python")[1].split("```")[0].strip()
    elif "```" in content:
        code_block = content.split("```")[1].strip()
        
    return {
        "messages": [response],
        "current_patch": code_block,
        "iterations": state.get("iterations", 0) + 1
    }
