from typing import TypedDict, List, Annotated, Optional
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    
    cve_id: str
    repo_path: str
    rag_context: str
    
    current_patch: Optional[str]
    test_results: Optional[str]
    error_analysis: Optional[str]
    sast_issues: Optional[List[str]]
    
    iterations: int
