from typing import Any, Dict
import os
from langchain_core.messages import SystemMessage, HumanMessage
from autosec.agent.state import AgentState
from autosec.agent.llm import get_llm

llm = get_llm(temperature=0)

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".go": "Go",
    ".rs": "Rust",
    ".sql": "SQL"
}

def coder_node(state: AgentState) -> Dict[str, Any]:
    print("--- CODER NODE ---")
    
    file_path = state.get("repo_path", "")
    _, ext = os.path.splitext(file_path)
    lang = LANGUAGE_MAP.get(ext, "Polyglot")
    
    CODER_PROMPT = f"""You are a generic {lang} Security Engineer. Implement the fix from the plan.

Rules:
1. Return ONLY the fixed code block.
2. For non-Python files, return the FULL file content if it ensures correctness.
3. Validate inputs and avoid injection flaws.

Return code in ```{ext[1:] if ext else 'text'} blocks."""
    
    messages = state['messages']
    last_message = messages[-1]
    cve_id = state['cve_id']
    sast_issues = state.get('sast_issues', [])
    err_analysis = state.get('error_analysis')
    
    if err_analysis or sast_issues:
        issues = "\n".join(sast_issues) if sast_issues else "None"
        prompt = f"Fix failed.\nFeedback: {err_analysis}\nSAST: {issues}\n\nRetry fix."
    else:
        prompt = f"CVE: {cve_id}\nPlan: {last_message.content}\n\nImplement safe {lang} code."

    response = llm.invoke([
        SystemMessage(content=CODER_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    content = response.content
    code_block = content
    
    # Generic markdown block extraction
    if "```" in content:
        parts = content.split("```")
        if len(parts) >= 3:
            # Usually: text ```lang code ``` text
            code_block = parts[1]
            if "\n" in code_block:
                code_block = code_block.split("\n", 1)[1] # Drop "python"/"cpp" line
    
    return {
        "messages": [response],
        "current_patch": code_block.strip(),
        "iterations": state.get("iterations", 0) + 1
    }
