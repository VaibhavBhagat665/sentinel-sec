from typing import Any, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from autosec.agent.state import AgentState
from autosec.agent.llm import get_llm
from autosec.rag.retriever import get_rag_context

llm = get_llm(temperature=0)

PLANNER_PROMPT = """You are a Security Architect. Analyze the vulnerability and create a remediation plan.

Output format:
1. Vulnerability Type
2. Attack Vector  
3. Affected Component
4. Fix Strategy"""

def planner_node(state: AgentState) -> Dict[str, Any]:
    print("--- PLANNER NODE ---")
    
    cve_id = state['cve_id']
    user_context = state['rag_context']
    
    rag_context = get_rag_context(user_context)
    full_context = f"{user_context}\n\n{rag_context}" if rag_context else user_context
    
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=f"CVE: {cve_id}\nContext: {full_context}")
    ]
    
    response = llm.invoke(messages)
    return {"messages": [response]}
