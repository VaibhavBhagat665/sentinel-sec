from pydantic import BaseModel
from typing import Optional, List

class PatchOutput(BaseModel):
    target_function: str
    patched_code: str
    explanation: str

class PlanOutput(BaseModel):
    vulnerability_type: str
    attack_vector: str
    remediation_steps: List[str]
    
class ReflectionOutput(BaseModel):
    error_analysis: str
    suggested_fix: str
    confidence: float
